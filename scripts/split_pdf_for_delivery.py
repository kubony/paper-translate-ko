#!/usr/bin/env python3
"""Split a PDF into page-range chunks that stay below an attachment-size limit."""

import argparse
import sys
from pathlib import Path

import fitz  # PyMuPDF


def render_range(source: fitz.Document, start: int, end: int) -> bytes:
    """Return inclusive zero-based page range as optimized PDF bytes."""
    chunk = fitz.open()
    chunk.insert_pdf(source, from_page=start, to_page=end)
    metadata = dict(source.metadata or {})
    if metadata:
        chunk.set_metadata(metadata)
    data = chunk.tobytes(garbage=4, deflate=True, clean=True)
    chunk.close()
    return data


def split_pdf(input_pdf: Path, output_dir: Path, max_bytes: int) -> list[tuple[Path, int, int, int]]:
    if max_bytes <= 0:
        raise ValueError("max_bytes must be positive")
    output_dir.mkdir(parents=True, exist_ok=True)

    source = fitz.open(input_pdf)
    try:
        if source.page_count == 0:
            raise ValueError("input PDF has no pages")

        ranges: list[tuple[int, int, bytes]] = []
        start = 0
        while start < source.page_count:
            single = render_range(source, start, start)
            if len(single) > max_bytes:
                raise ValueError(
                    f"page {start + 1} alone is {len(single):,} bytes, above the "
                    f"{max_bytes:,}-byte limit"
                )

            low, high = start, source.page_count - 1
            best_end, best_data = start, single
            while low <= high:
                mid = (low + high) // 2
                data = render_range(source, start, mid)
                if len(data) <= max_bytes:
                    best_end, best_data = mid, data
                    low = mid + 1
                else:
                    high = mid - 1

            ranges.append((start, best_end, best_data))
            start = best_end + 1

        width = max(2, len(str(len(ranges))))
        results = []
        for index, (start, end, data) in enumerate(ranges, 1):
            name = (
                f"{input_pdf.stem}_part{index:0{width}d}-of-{len(ranges):0{width}d}"
                f"_pages-{start + 1:03d}-{end + 1:03d}.pdf"
            )
            path = output_dir / name
            path.write_bytes(data)
            results.append((path, start + 1, end + 1, len(data)))
        return results
    finally:
        source.close()


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Split a PDF into page-range chunks below a delivery size limit."
    )
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument(
        "--max-mib",
        type=float,
        default=8.0,
        help="maximum size per part in MiB (default: 8.0, Discord-safe)",
    )
    args = parser.parse_args(argv)

    try:
        results = split_pdf(
            args.input_pdf,
            args.output_dir,
            max_bytes=int(args.max_mib * 1024 * 1024),
        )
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"[split] ERROR: {exc}", file=sys.stderr)
        return 1

    for path, start, end, size in results:
        print(f"[split] {path} | pages {start}-{end} | {size:,} bytes")
    print(f"[split] complete: {len(results)} part(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
