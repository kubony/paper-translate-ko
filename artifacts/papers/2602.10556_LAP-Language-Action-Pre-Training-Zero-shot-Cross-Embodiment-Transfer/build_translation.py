#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
import html, json, re

BASE = Path(__file__).resolve().parent
REPO = BASE.parents[2]
TITLE = "Language-Action Pre-Training Enables Zero-shot Cross-Embodiment Transfer"
KO_TITLE = "Language-Action Pre-Training: Zero-shot Cross-Embodiment Transfer의 실현"
AUTHORS = "Zhaoyang Li, Asher J. Hancock, Parker Ewen, Yiyang Zhu, Sriram Yenamandra, Yunhao Ge, Yilun Du, Shuran Song, Pieter Abbeel, Deepak Pathak, Jitendra Malik"
PARTS = [
    "part1_front_intro_related.html", "part2_method.html",
    "exp-a.html", "exp-b.html", "exp-c.html",
    "app-a.html", "app-b.html", "app-c.html", "references.html",
]

def read(path):
    return Path(path).read_text(encoding="utf-8")

def video_appendix():
    data = json.loads(read(BASE / "assets/videos.json"))
    cards = []
    for i, a in enumerate(data.get("assets", []), 1):
        src = a.get("remote_url") or a.get("local") or a.get("url")
        original = a.get("url", src)
        thumb = a.get("thumbnail", "")
        raw = Path(original.split("?")[0]).stem
        label = raw.replace("_", " ").replace("-", " ")
        duration = a.get("duration_s")
        meta = f"{duration:.1f}초" if isinstance(duration, (int, float)) else "영상"
        cards.append(f'''<article class="video-tile">
<a href="{html.escape(src)}"><img src="{html.escape(thumb)}" alt="프로젝트 영상 {i}: {html.escape(label)}"></a>
<div><b>영상 {i}.</b> {html.escape(label)}</div>
<div class="video-links">{meta} · <a href="{html.escape(src)}">GCS 보관본</a> · <a href="{html.escape(original)}">원본</a></div>
</article>''')
    return f'''<section class="video-appendix">
<h2 class="section">프로젝트 영상 자산</h2>
<p>공식 프로젝트 페이지에서 수집한 영상 32개다. PDF에서는 썸네일을 클릭하면 GCS 보관본을 열 수 있으며, 각 항목에 공식 원본 링크도 함께 제공한다.</p>
<div class="video-grid">{''.join(cards)}</div>
</section>'''

def main():
    template = BeautifulSoup(read(REPO / "assets/template.html"), "html.parser")
    css = template.style.string or ""
    extra = '''
      h2 { column-span: all; font-size: 15pt; font-weight: 800; margin: 14px 0 8px; padding: 5px 0; border-top: 1px solid #bbb; border-bottom: 1px solid #bbb; }
      section section h2, section section h3 { column-span: none; border: 0; padding: 0; }
      figure.fig-wide, table.wide, .video-appendix { column-span: all; }
      figure img { width: 100%; max-height: 205mm; object-fit: contain; }
      figure[data-figure="6"] img, figure[data-figure="7"] img, figure[data-figure="10"] img, figure[data-figure="11"] img { max-height: 120mm; }
      caption { caption-side: top; text-align: left; margin-bottom: 4px; font-size: 8.3pt; }
      .small-caps { font-variant: small-caps; }
      .body > section { break-inside: auto; }
      ol, ul { margin-top: 3px; padding-left: 18px; }
      li { margin-bottom: 3px; }
      .source-card { column-span: all; background: #f4f6f8; border-left: 4px solid #111; padding: 9px 12px; margin: 0 0 12px; }
      .video-appendix { page-break-before: always; }
      .video-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
      .video-tile { border: 1px solid #ccc; padding: 5px; break-inside: avoid; font-size: 7.7pt; text-align: left; }
      .video-tile img { width: 100%; aspect-ratio: 16/9; object-fit: cover; display:block; margin-bottom:4px; }
      .video-links { color:#555; font-size:7pt; }
      a { color: #174a85; text-decoration: none; }
      @media print { a { color: #111; } }
    '''
    shell = BeautifulSoup(f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{TITLE} — 한국어 전문 번역</title><style>{css}{extra}</style></head><body>
<section class="cover"><div class="bar"></div><div class="spacer"></div>
<h1>{TITLE}</h1><div class="subtitle">{KO_TITLE}<br>한국어 전문 번역</div>
<div class="meta"><div><b>저자</b>: {AUTHORS}</div><div><b>문서</b>: arXiv:2602.10556v2</div><div><b>원문</b>: https://arxiv.org/abs/2602.10556v2</div><div><b>번역 생성일</b>: 2026-07-27</div><div><b>번역·편집</b>: 제니 (Jennie)</div></div>
<div class="note">원문 LaTeX 구조를 기준으로 초록, 본문, 표, 수식, 그림, 전체 부록을 한국어로 재구성했다. 모델명·데이터셋명·수치·단위는 원문을 보존한다.</div></section>
<div class="body"><h1 class="doc-title">{TITLE} — 한국어 전체 번역</h1>
<div class="source-card"><b>원문:</b> <a href="https://arxiv.org/abs/2602.10556v2">arXiv v2</a> · <b>프로젝트:</b> <a href="https://lap-vla.github.io/">lap-vla.github.io</a> · <b>코드:</b> <a href="https://github.com/lihzha/lap">GitHub</a><br>
<b>번역 메모:</b> VLA, policy, action, action chunk, flow matching, cross-embodiment, embodiment, fine-tuning, zero-shot 등 핵심 전문용어는 영문 또는 혼합 표기를 사용한다.</div></div></body></html>''', "html.parser")
    body = shell.select_one("div.body")
    for name in PARTS:
        frag = BeautifulSoup(read(BASE / "drafts" / name), "html.parser")
        for node in list(frag.contents):
            body.append(node)
    body.append(BeautifulSoup(video_appendix(), "html.parser"))

    # Major section numbering and print classes.
    mapping = {
        "LAP: VLA를 위한 Language-Action Pre-Training": "3. LAP: VLA를 위한 Language-Action Pre-Training",
        "실험": "4. 실험",
        "결론 및 논의": "5. 결론 및 논의",
    }
    for h in shell.find_all(["h2", "h3", "h4"]):
        txt = h.get_text(" ", strip=True)
        if txt in mapping:
            h.string = mapping[txt]
        if h.name == "h2":
            h["class"] = sorted(set(h.get("class", []) + ["section"]))

    # Insert exact source figures 1..12.
    for fig in shell.find_all("figure", attrs={"data-figure": True}):
        n = int(fig["data-figure"])
        for placeholder in fig.select(".figure-placeholder"):
            placeholder.decompose()
        img = shell.new_tag("img", src=f"figures/final/fig{n}.png")
        img["alt"] = f"원문 그림 {n}"
        caption = fig.find("figcaption")
        if caption: caption.insert_before(img)
        else: fig.append(img)
        fig["class"] = sorted(set(fig.get("class", []) + ["fig-wide"]))

    for table in shell.find_all("table", attrs={"data-table": True}):
        cols = max((len(r.find_all(["th", "td"])) for r in table.find_all("tr")), default=0)
        if cols >= 6:
            table["class"] = sorted(set(table.get("class", []) + ["wide"]))

    out = BASE / "2602.10556_ko_translation_layout.html"
    out.write_text(str(shell), encoding="utf-8")
    print(out)
    print({
        "figures": len(shell.find_all("figure", attrs={"data-figure": True})),
        "tables": len(shell.find_all("table", attrs={"data-table": True})),
        "equations": len(shell.find_all("pre", class_="equation")),
        "videos": len(shell.select(".video-tile")),
        "references": len(shell.select("ol.refs > li")),
    })

if __name__ == "__main__":
    main()
