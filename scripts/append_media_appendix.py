#!/usr/bin/env python3
"""번역 HTML 끝에 「부록. 원문 영상 자산」 섹션을 붙인다.

원문이 웹 문서면 영상이 근거의 일부다. 원문 페이지가 내려가도 재생할 수 있도록
GCS에 미러링한 사본(`remote_url`)을 링크하고, 썸네일과 한국어 캡션을 함께 싣는다.

자산 매니페스트는 번역 작업 폴더가 아니라 **자산 보관 폴더**에서 읽는다.
재번역으로 translation.html을 새로 쓰더라도 이미 미러링해 둔 자산을 그대로
재사용하기 위해서다.

사용법:
    python3 append_media_appendix.py <translation.html> <자산폴더> [--title 제목]

    <자산폴더>는 `assets/videos.json`(+ 선택적으로 `assets/captions.ko.json`,
    `assets/videos/thumbs/*.jpg`)을 담은 디렉토리다.

이미 부록이 있으면 통째로 교체한다(멱등). videos.json에 `remote_url`이 없는
자산은 재생 근거가 되지 못하므로 건너뛰고, 건너뛴 개수를 보고한다.
"""
import argparse
import html
import json
import os
import re
import sys

APPENDIX_MARK = "media-appendix"
APPENDIX_RE = re.compile(
    r'\n*<section[^>]*class="[^"]*\bmedia-appendix\b[^"]*"[\s\S]*?</section>\n*',
    re.IGNORECASE,
)


def _fmt_duration(seconds):
    if not seconds:
        return ""
    total = int(round(float(seconds)))
    return f"{total // 60}:{total % 60:02d}"


def _fmt_size(num_bytes):
    if not num_bytes:
        return ""
    mib = float(num_bytes) / (1024 * 1024)
    return f"{mib:.1f} MB" if mib >= 0.1 else "<0.1 MB"


def build_appendix(assets_dir, html_dir, title):
    """자산 매니페스트를 읽어 부록 HTML 문자열과 통계를 만든다."""
    manifest_path = os.path.join(assets_dir, "assets", "videos.json")
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    captions = {}
    captions_path = os.path.join(assets_dir, "assets", "captions.ko.json")
    if os.path.exists(captions_path):
        with open(captions_path, encoding="utf-8") as f:
            captions = json.load(f)

    rows, skipped = [], 0
    for asset in manifest.get("assets", []):
        remote = asset.get("remote_url")
        if not remote:
            skipped += 1
            continue

        local = asset.get("local") or ""
        basename = os.path.basename(local) or os.path.basename(asset.get("url", ""))
        caption = captions.get(basename) or asset.get("title") or basename

        thumb_cell = ""
        thumb_rel = asset.get("thumbnail")
        if thumb_rel:
            thumb_abs = os.path.join(assets_dir, thumb_rel)
            if os.path.exists(thumb_abs):
                src = os.path.relpath(thumb_abs, html_dir)
                # 썸네일은 목록의 식별용이다. 크기를 묶지 않으면 원본 해상도로
                # 렌더돼 한 행이 페이지를 통째로 차지한다(실제로 자산 3개가 13쪽이 됐다).
                thumb_cell = (
                    f'<img src="{html.escape(src)}" alt="" '
                    'style="max-width:96px;max-height:64px;object-fit:cover;">'
                )

        meta = " · ".join(x for x in (_fmt_duration(asset.get("duration_s")),
                                      _fmt_size(asset.get("bytes"))) if x)
        origin = asset.get("url", "")
        rows.append(
            "<tr>"
            f'<td class="thumb">{thumb_cell}</td>'
            f"<td>{html.escape(caption)}"
            + (f'<br><span class="meta">{html.escape(meta)}</span>' if meta else "")
            + "</td>"
            f'<td><a href="{html.escape(remote)}">보관 사본</a>'
            + (f'<br><a href="{html.escape(origin)}">원본</a>' if origin else "")
            + "</td></tr>"
        )

    if not rows:
        return None, 0, skipped

    section = (
        f'\n<section class="{APPENDIX_MARK}">\n'
        "<style>\n"
        ".media-appendix table.media-assets td { vertical-align: top; }\n"
        ".media-appendix table.media-assets tr { page-break-inside: avoid; }\n"
        ".media-appendix td.thumb { width: 104px; }\n"
        ".media-appendix .meta { color: #666; font-size: 0.85em; }\n"
        "</style>\n"
        f"<h2>{html.escape(title)}</h2>\n"
        '<p class="note">원문 페이지의 영상·애니메이션이다. 원문이 내려가도 근거를 '
        "확인할 수 있도록 보관 사본을 함께 링크했다.</p>\n"
        '<table class="wide media-assets">\n'
        "<thead><tr><th>미리보기</th><th>설명</th><th>링크</th></tr></thead>\n"
        "<tbody>\n" + "\n".join(rows) + "\n</tbody>\n</table>\n</section>\n"
    )
    return section, len(rows), skipped


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html_path")
    parser.add_argument("assets_dir")
    parser.add_argument("--title", default="부록. 원문 영상 자산")
    args = parser.parse_args(argv)

    html_dir = os.path.dirname(os.path.abspath(args.html_path))
    section, n_rows, n_skipped = build_appendix(args.assets_dir, html_dir, args.title)
    if section is None:
        print(f"[appendix] remote_url을 가진 자산이 없다 — 건너뛴다 ({args.assets_dir})")
        return 1

    with open(args.html_path, encoding="utf-8") as f:
        raw = f.read()

    raw, n_removed = APPENDIX_RE.subn("\n", raw)
    if "</body>" in raw:
        raw = raw.replace("</body>", section + "</body>", 1)
    else:
        raw = raw + section

    with open(args.html_path, "w", encoding="utf-8") as f:
        f.write(raw)

    action = "교체" if n_removed else "추가"
    note = f", remote_url 없어 제외 {n_skipped}개" if n_skipped else ""
    print(f"[appendix] {action}: 자산 {n_rows}개{note} → {args.html_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
