#!/usr/bin/env python3
"""Static preflight for Chrome multi-column heading/wide-element layout.

Fails when an HTML document contains h2.section/h3.section headings or wide
TABLE/FIGURE elements but the embedded CSS does not place the corresponding
selector in a `column-span: all` rule. This catches a real failure where the
last word of a wide table title was printed in the opposite column.
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


def spanning_selectors(html: str) -> set[str]:
    selectors: set[str] = set()
    style_blocks = re.findall(r"<style\b[^>]*>(.*?)</style>", html, flags=re.I | re.S)
    css = "\n".join(style_blocks) if style_blocks else html
    for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", css, flags=re.S):
        selector_text, declarations = match.groups()
        normalized = re.sub(r"\s+", " ", declarations).lower()
        if not re.search(r"column-span\s*:\s*all", normalized):
            continue
        for selector in selector_text.split(","):
            selectors.add(re.sub(r"\s+", " ", selector.strip()))
    return selectors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("html", type=Path)
    args = parser.parse_args()

    text = args.html.read_text(encoding="utf-8")
    inv = Inventory()
    inv.feed(text)
    selectors = spanning_selectors(text)

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

    print("Inventory:")
    for key, value in inv.counts.items():
        print(f"  {key}: {value}")
    print("Spanning selectors:", ", ".join(sorted(selectors)) or "(none)")

    if errors:
        print("FAIL:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print("PASS: multi-column wide-element static preflight")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
