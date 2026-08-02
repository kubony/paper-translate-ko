#!/usr/bin/env python3
"""Static preflight for Chrome multi-column and print-separator layout.

Fails when an HTML document contains h2.section/h3.section headings or wide
TABLE/FIGURE elements but the embedded CSS does not place the corresponding
selector in a `column-span: all` rule. This catches a real failure where the
last word of a wide table title was printed in the opposite column.

Also rejects two Chromium print regressions observed in production dossiers:

* an active ``column-rule`` combined with ``column-span: all`` elements, which
  can leave vertical rule fragments through headings and metadata strips;
* a cover separator drawn by an absolutely positioned pseudo-element at a
  fixed physical offset, which can cross a wrapped title.
"""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class Inventory(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.counts = {
            "h2.section": 0,
            "h3.section": 0,
            "table.wide": 0,
            "figure.fig-wide": 0,
        }

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        class_attr = dict(attrs).get("class") or ""
        classes = set(class_attr.split())
        key = f"{tag}.section"
        if tag in {"h2", "h3"} and "section" in classes:
            self.counts[key] += 1
        if tag == "table" and "wide" in classes:
            self.counts["table.wide"] += 1
        if tag == "figure" and "fig-wide" in classes:
            self.counts["figure.fig-wide"] += 1


def css_rules(html: str) -> list[tuple[str, str]]:
    """Return flat selector/declaration pairs from embedded or raw CSS."""
    style_blocks = re.findall(r"<style\b[^>]*>(.*?)</style>", html, flags=re.I | re.S)
    css = "\n".join(style_blocks) if style_blocks else html
    return [
        (re.sub(r"\s+", " ", selector.strip()), declarations)
        for selector, declarations in re.findall(r"([^{}]+)\{([^{}]*)\}", css, flags=re.S)
    ]


def spanning_selectors(html: str) -> set[str]:
    selectors: set[str] = set()
    for selector_text, declarations in css_rules(html):
        normalized = re.sub(r"\s+", " ", declarations).lower()
        if not re.search(r"column-span\s*:\s*all", normalized):
            continue
        for selector in selector_text.split(","):
            selectors.add(re.sub(r"\s+", " ", selector.strip()))
    return selectors


def active_column_rules(html: str) -> list[tuple[str, str]]:
    """Find non-zero/non-none column-rule shorthands."""
    found: list[tuple[str, str]] = []
    for selector, declarations in css_rules(html):
        for value in re.findall(r"column-rule\s*:\s*([^;}]+)", declarations, flags=re.I):
            normalized = re.sub(r"\s+", " ", value.strip().lower())
            if normalized not in {"none", "0", "0px", "0pt", "0mm"}:
                found.append((selector, normalized))
    return found


def fixed_cover_separators(html: str) -> list[str]:
    """Find cover pseudo-element rules whose line position ignores title flow."""
    found: list[str] = []
    for selector, declarations in css_rules(html):
        lowered_selector = selector.lower()
        normalized = re.sub(r"\s+", " ", declarations).lower()
        if (
            "cover" in lowered_selector
            and re.search(r":{1,2}(?:before|after)\b", lowered_selector)
            and re.search(r"position\s*:\s*(?:absolute|fixed)", normalized)
            and re.search(r"(?:^|;)\s*(?:top|bottom)\s*:", normalized)
            and re.search(r"(?:height|border|background)\s*:", normalized)
        ):
            found.append(selector)
    return found


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("html", type=Path)
    args = parser.parse_args()

    text = args.html.read_text(encoding="utf-8")
    inv = Inventory()
    inv.feed(text)
    selectors = spanning_selectors(text)
    column_rules = active_column_rules(text)
    cover_separators = fixed_cover_separators(text)

    errors: list[str] = []
    coverage = {
        "h2.section": {"h2.section", ".section"},
        "h3.section": {"h3.section", ".section"},
        "table.wide": {"table.wide", ".wide"},
        "figure.fig-wide": {"figure.fig-wide", ".fig-wide"},
    }
    for element, accepted in coverage.items():
        if inv.counts[element] and not (accepted & selectors):
            errors.append(
                f"{element}: {inv.counts[element]} elements exist but no applicable "
                "column-span: all selector was found; accepted selectors: "
                + ", ".join(sorted(accepted))
            )

    spanning_count = sum(inv.counts.values())
    if spanning_count and column_rules:
        rendered = ", ".join(f"{selector} ({value})" for selector, value in column_rules)
        errors.append(
            "active column-rule with column-span:all content can fragment through "
            f"headings/metadata in Chromium print: {rendered}; use column-rule:none"
        )
    if cover_separators:
        errors.append(
            "flow-independent cover separator found on "
            + ", ".join(cover_separators)
            + "; attach the line to the title with border-bottom/padding instead of a fixed top/bottom offset"
        )

    print("Inventory:")
    for key, value in inv.counts.items():
        print(f"  {key}: {value}")
    print("Spanning selectors:", ", ".join(sorted(selectors)) or "(none)")
    print("Active column rules:", ", ".join(f"{s} ({v})" for s, v in column_rules) or "(none)")
    print("Fixed cover separators:", ", ".join(cover_separators) or "(none)")

    if errors:
        print("FAIL:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("PASS: multi-column wide-element and separator static preflight")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
