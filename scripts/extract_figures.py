#!/usr/bin/env python3
"""원본 PDF에서 그림 영역을 이미지로 추출한다 (pymupdf/fitz).

반드시 uv로 실행한다 (시스템 pip는 PEP 668로 막혀 있음):
    uv run --quiet --with pymupdf python3 extract_figures.py auto <pdf> <outdir>
    uv run --quiet --with pymupdf python3 extract_figures.py crop <pdf> <page> <x0> <y0> <x1> <y1> <out.png> [zoom]

모드:
  auto  <pdf> <outdir>
        (a) 각 페이지를 zoom 2로 렌더해 <outdir>/pages/page-NN.png 로 저장한다.
            에이전트가 눈으로 그림 위치를 확인하는 용도.
        (b) 페이지별로 raster 이미지 bbox와 stroke/fill이 있는 벡터 드로잉 bbox를
            모아 인접(30pt 이내)한 것끼리 클러스터링하고, 잡음 클러스터를 버린 뒤
            각 클러스터를 zoom 3으로 클립 렌더해 <outdir>/fig-pNN-KK.png 로 저장한다.
            클러스터 bbox 표를 stdout에 출력한다.

  crop  <pdf> <page_1based> <x0> <y0> <x1> <y1> <out.png> [zoom=3]
        PDF 포인트 좌표로 수동 크롭 렌더. auto가 그림을 잘못 자를 때
        pages/page-NN.png(zoom 2, 즉 픽셀/2 = 포인트)를 보고 좌표를 계산해 쓴다.
"""
import os
import sys

import fitz  # pymupdf


# ---- 클러스터링 파라미터 --------------------------------------------------
MERGE_GAP = 30.0        # 이 거리(pt) 이내면 같은 그림으로 병합
MIN_AREA_FRAC = 0.01    # 페이지 면적의 1% 미만 클러스터는 버린다
MIN_TEXT_ONLY_H = 30.0  # raster 이미지가 없고 높이가 이보다 작으면 버린다(괘선/밑줄 노이즈)


def _rect_near(a, b, gap):
    """두 사각형이 gap 이내로 겹치거나 인접하면 True."""
    return not (
        a[2] < b[0] - gap or  # a가 b의 왼쪽
        a[0] > b[2] + gap or  # a가 b의 오른쪽
        a[3] < b[1] - gap or  # a가 b의 위쪽
        a[1] > b[3] + gap     # a가 b의 아래쪽
    )


def _union(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


def _collect_boxes(page):
    """(bbox, is_raster) 리스트를 모은다."""
    boxes = []
    # raster 이미지
    try:
        for info in page.get_image_info():
            bb = info.get("bbox")
            if bb:
                boxes.append((tuple(bb), True))
    except Exception:
        pass
    # 벡터 드로잉: stroke 또는 fill 이 실제로 있는 것만
    try:
        for d in page.get_drawings():
            if not (d.get("stroke") or d.get("fill")):
                continue
            bb = d.get("rect")
            if bb:
                boxes.append((tuple(bb), False))
    except Exception:
        pass
    return boxes


def _cluster(boxes):
    """근접 박스를 union-find 식으로 병합. 각 클러스터의 raster 포함 여부를 함께 반환."""
    rects = [list(b[0]) for b in boxes]
    has_raster = [b[1] for b in boxes]
    parent = list(range(len(rects)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        parent[find(i)] = find(j)

    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            if _rect_near(rects[i], rects[j], MERGE_GAP):
                union(i, j)

    groups = {}
    for i in range(len(rects)):
        r = find(i)
        if r not in groups:
            groups[r] = {"box": tuple(rects[i]), "raster": has_raster[i]}
        else:
            groups[r]["box"] = _union(groups[r]["box"], rects[i])
            groups[r]["raster"] = groups[r]["raster"] or has_raster[i]
    return list(groups.values())


def auto(pdf_path, outdir):
    os.makedirs(outdir, exist_ok=True)
    pages_dir = os.path.join(outdir, "pages")
    os.makedirs(pages_dir, exist_ok=True)
    doc = fitz.open(pdf_path)

    rows = []
    for pno in range(len(doc)):
        page = doc[pno]
        pw, ph = page.rect.width, page.rect.height
        page_area = pw * ph

        # (a) 페이지 전체 렌더 (zoom 2)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        page_png = os.path.join(pages_dir, f"page-{pno + 1:02d}.png")
        pix.save(page_png)

        # (b) 그림 클러스터
        boxes = _collect_boxes(page)
        clusters = _cluster(boxes)

        kept = []
        for c in clusters:
            x0, y0, x1, y1 = c["box"]
            # 페이지 경계로 클램프
            x0, y0 = max(0, x0), max(0, y0)
            x1, y1 = min(pw, x1), min(ph, y1)
            w, h = x1 - x0, y1 - y0
            if w <= 1 or h <= 1:
                continue
            area = w * h
            if area < page_area * MIN_AREA_FRAC:
                continue
            # raster 없고 얇은 것(괘선/밑줄) 버림
            if not c["raster"] and h < MIN_TEXT_ONLY_H:
                continue
            kept.append((x0, y0, x1, y1, c["raster"]))

        # 같은 페이지 안에서 위->아래 정렬
        kept.sort(key=lambda r: (r[1], r[0]))
        for kk, (x0, y0, x1, y1, is_raster) in enumerate(kept, start=1):
            clip = fitz.Rect(x0, y0, x1, y1)
            fig_pix = page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=clip)
            fname = f"fig-p{pno + 1:02d}-{kk:02d}.png"
            fig_pix.save(os.path.join(outdir, fname))
            rows.append((pno + 1, x0, y0, x1, y1, "raster" if is_raster else "vector", fname))

    doc.close()

    # 표 출력
    print(f"\n페이지 렌더: {pages_dir}/page-NN.png (zoom 2)")
    print(f"그림 후보: {outdir}/fig-pNN-KK.png (zoom 3)\n")
    print(f"{'page':>4} {'x0':>7} {'y0':>7} {'x1':>7} {'y1':>7} {'kind':>7}  file")
    print("-" * 72)
    for r in rows:
        print(f"{r[0]:>4} {r[1]:>7.1f} {r[2]:>7.1f} {r[3]:>7.1f} {r[4]:>7.1f} {r[5]:>7}  {r[6]}")
    if not rows:
        print("(그림 후보 없음 — pages/ PNG를 보고 crop 모드로 수동 추출하라)")
    print(f"\n총 {len(rows)}개 그림 후보 추출됨.")


def crop(pdf_path, page_1based, x0, y0, x1, y1, out_png, zoom=3.0):
    doc = fitz.open(pdf_path)
    page = doc[int(page_1based) - 1]
    clip = fitz.Rect(float(x0), float(y0), float(x1), float(y1))
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip)
    os.makedirs(os.path.dirname(os.path.abspath(out_png)), exist_ok=True)
    pix.save(out_png)
    doc.close()
    print(f"[crop] page {page_1based} {clip} zoom={zoom} -> {out_png} "
          f"({pix.width}x{pix.height}px)")


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    mode = argv[1]
    if mode == "auto":
        if len(argv) != 4:
            print("사용법: auto <pdf> <outdir>")
            return 1
        auto(argv[2], argv[3])
    elif mode == "crop":
        if len(argv) not in (9, 10):
            print("사용법: crop <pdf> <page_1based> <x0> <y0> <x1> <y1> <out.png> [zoom]")
            return 1
        zoom = float(argv[9]) if len(argv) == 10 else 3.0
        crop(argv[2], argv[3], argv[4], argv[5], argv[6], argv[7], argv[8], zoom)
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
