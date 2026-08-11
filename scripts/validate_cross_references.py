#!/usr/bin/env python3
"""Validate translated figure cross-references against canonical LaTeX labels.

The translated HTML must preserve every prose figure reference as an element like:

    <a class="xref" data-source-ref="fig:arch" href="#fig-2">그림 2</a>

Every rendered figure must expose its canonical source label:

    <figure id="fig-2" data-source-label="fig:arch" data-figure="2">...</figure>

Usage:
    python3 scripts/validate_cross_references.py source/main.tex translation.html
"""

from __future__ import annotations

import argparse
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re


TOKEN_RE = re.compile(
    r"\\setcounter\{figure\}\{(?P<set>\d+)\}"
    r"|\\addtocounter\{figure\}\{(?P<add>-?\d+)\}"
    r"|\\renewcommand\*?\{\\thefigure\}\{(?P<literal>[^}]+)\}"
    r"|\\begin\{(?P<begin_env>figure\*?|wrapfigure)\}(?:\{[^}]*\})?"
    r"|\\end\{(?P<end_env>figure\*?|wrapfigure)\}"
    r"|\\captionsetup\{type=figure\}"
    r"|\\captionof\{figure\}"
    r"|\\caption(?P<caption_star>\*)?\s*\{"
    r"|\\label\{(?P<label>[^}]+)\}"
)
REF_RE = re.compile(r"\\(?:auto|page)?ref\{([^}]+)\}")
DISPLAY_NUMBER_RE = re.compile(r"(?:그림|Figure|Fig\.)\s*([A-Za-z]?\d+)", re.IGNORECASE)


def _strip_comments(source: str) -> str:
    """Remove unescaped LaTeX comments while preserving line boundaries."""
    return re.sub(r"(?<!\\)%[^\n]*", "", source)


def resolve_figure_numbers(source: str) -> dict[str, int | str]:
    """Resolve figure labels using LaTeX counter mutations and caption order."""
    source = _strip_comments(source)
    counter = 0
    figure_depth = 0
    force_next_caption = False
    synthetic_label_pending = False
    current_number: int | str | None = None
    literal_next: str | None = None
    labels: dict[str, int | str] = {}

    for match in TOKEN_RE.finditer(source):
        token = match.group(0)
        if match.group("set") is not None:
            counter = int(match.group("set"))
            current_number = None
            synthetic_label_pending = False
        elif match.group("add") is not None:
            counter += int(match.group("add"))
            current_number = None
            synthetic_label_pending = False
        elif match.group("literal") is not None:
            literal_next = match.group("literal")
            current_number = None
        elif match.group("begin_env") is not None:
            figure_depth += 1
            current_number = None
            synthetic_label_pending = False
        elif match.group("end_env") is not None:
            figure_depth = max(0, figure_depth - 1)
            current_number = None
        elif token == r"\captionsetup{type=figure}":
            force_next_caption = True
        elif token == r"\captionof{figure}":
            counter += 1
            current_number = literal_next or counter
            literal_next = None
            force_next_caption = False
            synthetic_label_pending = figure_depth == 0
        elif token.startswith(r"\caption"):
            is_synthetic = bool(force_next_caption and figure_depth == 0)
            if match.group("caption_star") is None and (figure_depth or force_next_caption):
                counter += 1
                current_number = literal_next or counter
                literal_next = None
                synthetic_label_pending = is_synthetic
            force_next_caption = False
        elif (
            match.group("label") is not None
            and current_number is not None
            and (figure_depth > 0 or synthetic_label_pending)
        ):
            label = match.group("label")
            if label in labels and labels[label] != current_number:
                raise ValueError(
                    f"figure label {label!r} resolves to both {labels[label]} and {current_number}"
                )
            labels[label] = current_number
            if synthetic_label_pending:
                synthetic_label_pending = False

    return labels


class _CrossReferenceHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.targets: dict[str, tuple[str | None, str | None]] = {}
        self.refs: list[dict[str, str | None]] = []
        self._active_refs: list[dict[str, object]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        source_label = attr_map.get("data-source-label")
        if source_label:
            self.targets[source_label] = (attr_map.get("id"), attr_map.get("data-figure"))

        source_ref = attr_map.get("data-source-ref")
        if source_ref:
            record: dict[str, object] = {
                "tag": tag,
                "label": source_ref,
                "href": attr_map.get("href"),
                "text_parts": [],
            }
            self._active_refs.append(record)

    def handle_data(self, data: str) -> None:
        for record in self._active_refs:
            text_parts = record["text_parts"]
            assert isinstance(text_parts, list)
            text_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self._active_refs) - 1, -1, -1):
            record = self._active_refs[index]
            if record["tag"] != tag:
                continue
            self._active_refs.pop(index)
            text_parts = record["text_parts"]
            assert isinstance(text_parts, list)
            self.refs.append(
                {
                    "label": str(record["label"]),
                    "href": None if record["href"] is None else str(record["href"]),
                    "text": "".join(str(part) for part in text_parts).strip(),
                }
            )
            break


def _source_reference_counts(source: str, labels: dict[str, int | str]) -> Counter[str]:
    return Counter(label for label in REF_RE.findall(_strip_comments(source)) if label in labels)


def validate_cross_references(source: str, html: str) -> list[str]:
    labels = resolve_figure_numbers(source)
    parser = _CrossReferenceHTMLParser()
    parser.feed(html)
    errors: list[str] = []

    for label, expected_number in labels.items():
        target = parser.targets.get(label)
        if target is None:
            errors.append(f"missing figure target for {label} (expected {expected_number})")
            continue
        target_id, data_number = target
        if target_id != f"fig-{expected_number}" or data_number != str(expected_number):
            errors.append(
                f"target drift for {label}: id={target_id!r}, data-figure={data_number!r}, "
                f"expected fig-{expected_number}/{expected_number}"
            )

    translated_counts: Counter[str] = Counter()
    for ref in parser.refs:
        label = ref["label"] or ""
        translated_counts[label] += 1
        if label not in labels:
            errors.append(f"unknown source figure label in HTML: {label}")
            continue
        expected_number = labels[label]
        text = ref["text"] or ""
        number_match = DISPLAY_NUMBER_RE.search(text)
        displayed_number = number_match.group(1) if number_match else None
        if displayed_number != str(expected_number):
            errors.append(
                f"display number drift for {label}: got {displayed_number!r}, expected {expected_number}"
            )
        expected_href = f"#fig-{expected_number}"
        if ref["href"] != expected_href:
            errors.append(
                f"href drift for {label}: got {ref['href']!r}, expected {expected_href!r}"
            )

    source_counts = _source_reference_counts(source, labels)
    if source_counts != translated_counts:
        all_labels = sorted(set(source_counts) | set(translated_counts))
        delta = ", ".join(
            f"{label}: source={source_counts[label]}, html={translated_counts[label]}"
            for label in all_labels
            if source_counts[label] != translated_counts[label]
        )
        errors.append(f"reference occurrence mismatch: {delta}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_tex", type=Path)
    parser.add_argument("translation_html", type=Path)
    args = parser.parse_args()

    errors = validate_cross_references(
        args.source_tex.read_text(encoding="utf-8"),
        args.translation_html.read_text(encoding="utf-8"),
    )
    if errors:
        for error in errors:
            print(f"[FAIL] {error}")
        print(f"cross-reference validation: FAIL ({len(errors)} errors)")
        return 1
    print("cross-reference validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
