from pathlib import Path
from bs4 import BeautifulSoup
import re

ROOT = Path(__file__).resolve().parent
fragments = [ROOT / f"fragment_{i}.html" for i in (1, 2, 3)]
body_html = "\n".join(p.read_text(encoding="utf-8") for p in fragments)
soup = BeautifulSoup(f'<div id="content">{body_html}</div>', "html.parser")
content = soup.select_one("#content")

# Preserve the source figure entities as exact publisher-supplied images.
for n in range(1, 14):
    fig = content.select_one(f"#figure-{n}")
    if fig is None:
        marker = None
        for c in content.find_all(string=lambda x: isinstance(x, str) and f"FIGURE {n}" in x):
            marker = c
            break
        if marker:
            fig = marker.find_next("figure")
    if fig is None:
        raise RuntimeError(f"figure {n} marker/entity missing")
    fig["id"] = f"figure-{n}"
    fig["class"] = sorted(set((fig.get("class") or []) + ["fig-wide"]))
    img = soup.new_tag("img", src=f"figures_exact/figure-{n:02d}.png")
    img["alt"] = f"원문 그림 {n}"
    fig.insert(0, img)

for h2 in content.find_all("h2"):
    h2["class"] = sorted(set((h2.get("class") or []) + ["section"]))
for table in content.find_all("table"):
    table["class"] = sorted(set((table.get("class") or []) + ["wide"]))

# Full source reference list, preserving bibliographic titles and identifiers.
source = BeautifulSoup(Path("/tmp/frontiers_838059.html").read_text(encoding="utf-8"), "html.parser")
ref_h = next(h for h in source.find_all("h2") if h.get_text(" ", strip=True) == "References")
ref_ul = ref_h.find_next_sibling("ul")
refs = []
for li in ref_ul.find_all("li", recursive=False):
    txt = " ".join(li.get_text(" ", strip=True).split())
    txt = re.sub(r"\s+(CrossRef|Google Scholar|View reference in article)(\s+(CrossRef|Google Scholar|View reference in article))*\s*$", "", txt)
    txt = re.sub(r"^\d+\s+", "", txt)
    if txt:
        refs.append(txt)
if len(refs) < 40:
    raise RuntimeError(f"reference extraction incomplete: {len(refs)}")
refs_html = "\n".join(f"<li>{BeautifulSoup('', 'html.parser').new_string(r)}</li>" for r in refs)

css = r'''
@page { size: A4; margin: 15mm; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
* { box-sizing: border-box; }
body { font-family: "Noto Sans KR", "Noto Sans CJK KR", "Apple SD Gothic Neo", sans-serif; color:#111; font-size:9.1pt; line-height:1.52; margin:0; }
a { color:#174d83; text-decoration:none; overflow-wrap:anywhere; }
.cover { position:relative; min-height:250mm; padding-left:14mm; page-break-after:always; }
.cover .bar { position:absolute; left:0; top:0; bottom:0; width:6px; background:#111; }
.cover .spacer { height:63mm; }
.cover h1 { font-size:26pt; font-weight:800; line-height:1.13; margin:0 0 8px; padding-bottom:11px; border-bottom:3px solid #111; max-width:155mm; }
.cover .ko-title { font-size:17pt; font-weight:750; margin:10px 0 3px; }
.cover .subtitle { font-size:12pt; font-weight:700; color:#315f86; margin:0 0 18px; }
.cover .meta { font-size:9.8pt; line-height:1.8; }
.cover .note { margin-top:18px; font-size:8.7pt; color:#666; max-width:150mm; }
.body { column-count:2; column-gap:7mm; column-fill:auto; text-align:justify; }
.body p { margin:0 0 7px; }
h1.doc-title { column-span:all; font-size:16.5pt; line-height:1.22; font-weight:800; margin:0 0 7px; padding-bottom:8px; border-bottom:2px solid #111; }
h2.section { column-span:all; font-size:14pt; font-weight:800; margin:13px 0 8px; padding:5px 0; border-top:1px solid #aaa; border-bottom:1px solid #aaa; break-after:avoid; }
h3 { font-size:10.8pt; font-weight:750; margin:9px 0 4px; break-after:avoid; }
h4 { font-size:9.6pt; font-weight:750; margin:8px 0 3px; break-after:avoid; }
ul.biblist, ul.memo { margin:0 0 8px; padding-left:16px; }
ul.biblist li, ul.memo li { margin-bottom:3px; }
.memo-title { font-size:11.5pt; font-weight:800; margin:7px 0 5px; }
pre.equation { font-family:"DejaVu Sans Mono", monospace; font-size:8.4pt; line-height:1.35; background:#f3f5f7; border:1px solid #ccd2d8; border-left:3px solid #315f86; border-radius:3px; padding:6px 8px; margin:7px 0; white-space:pre-wrap; word-break:break-word; break-inside:avoid; text-align:left; }
figure { margin:8px 0; text-align:center; break-inside:avoid; }
figure.fig-wide { column-span:all; }
figure img { max-width:100%; height:auto; max-height:220mm; object-fit:contain; }
figcaption { font-size:8.1pt; line-height:1.4; color:#444; margin-top:4px; text-align:left; }
table { width:100%; border-collapse:collapse; font-size:7.5pt; line-height:1.27; margin:7px 0 10px; break-inside:avoid; }
table.wide { column-span:all; }
caption { caption-side:top; text-align:left; font-size:8.3pt; margin:0 0 4px; }
th,td { border:.6pt solid #333; padding:2.5px 3px; text-align:center; vertical-align:middle; overflow-wrap:anywhere; }
th { background:#e9ecef; font-weight:700; }
.algorithm { column-span:all; border:1px solid #888; background:#fafafa; padding:8px 10px; margin:8px 0 10px; break-inside:avoid; }
.algorithm ol { margin:4px 0 0; padding-left:20px; }
.algorithm li { margin-bottom:3px; }
.refs-note { font-size:8.5pt; color:#555; }
ol.refs { margin:0; padding-left:18px; font-size:7.7pt; line-height:1.35; }
ol.refs li { margin-bottom:3px; break-inside:avoid; }
.license { column-span:all; font-size:8.2pt; color:#555; background:#f7f7f7; border-left:3px solid #777; padding:7px 9px; margin-top:10px; }
'''

html = f'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8">
<title>Visual Rewards From Observation for Sequential Tasks — 한국어 전문 번역</title>
<style>{css}</style></head><body>
<section class="cover"><div class="bar"></div><div class="spacer"></div>
<h1>Visual Rewards From Observation for Sequential Tasks: Autonomous Pile Loading</h1>
<div class="ko-title">순차 과제를 위한 관찰 기반 시각 보상: 자율 파일 로딩</div>
<div class="subtitle">한국어 전문 번역</div>
<div class="meta">
<div><b>저자</b>: Nataliya Strokina, Wenyan Yang, Joni Pajarinen, Nikolay Serbenyuk, Joni Kämäräinen, Reza Ghabcheloo</div>
<div><b>저널</b>: Frontiers in Robotics and AI, Vol. 9, Article 838059 (2022)</div>
<div><b>DOI</b>: 10.3389/frobt.2022.838059</div>
<div><b>원문</b>: https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2022.838059/full</div>
<div><b>번역 생성일</b>: 2026-08-02</div>
<div><b>번역·편집</b>: 제니 (Jennie)</div>
</div>
<div class="note">원문의 섹션 구조를 따라 초록부터 결론과 출판사 성명까지 완역했다. 원문 피겨 13개를 개별 자산으로 보존하고, 표 3개는 수치를 유지한 HTML 표로 재구성했다. 참고문헌의 서지 제목과 DOI는 원문 표기를 유지했다.</div>
</section>
<div class="body">
<h1 class="doc-title">Visual Rewards From Observation for Sequential Tasks: Autonomous Pile Loading — 한국어 전체 번역</h1>
<ul class="biblist">
<li><b>원문 제목</b>: Visual Rewards From Observation for Sequential Tasks: Autonomous Pile Loading</li>
<li><b>저자·소속</b>: Strokina et al.; Tampere University, Aalto University</li>
<li><b>저널</b>: Frontiers in Robotics and AI 9:838059; published 31 May 2022</li>
<li><b>DOI/PDF</b>: <a href="https://doi.org/10.3389/frobt.2022.838059">10.3389/frobt.2022.838059</a> · <a href="https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2022.838059/pdf">원문 PDF</a></li>
<li><b>라이선스</b>: Creative Commons Attribution (CC BY)</li>
</ul>
<div class="memo-title">번역 메모</div>
<ul class="memo">
<li><b>pile loading</b>은 제목에서 원문의 산업 용례를 살려 “파일 로딩”으로 두고, 본문에서는 문맥에 따라 “적재 더미 상차/로딩”으로 풀어 썼다.</li>
<li><b>reward</b>는 “보상”, <b>stage-based reward</b>는 “단계 기반 보상”, <b>terminal reward</b>는 “종단 보상”으로 옮겼다.</li>
<li><b>policy</b>와 <b>action</b>은 로봇 학습 문맥의 의미를 보존하기 위해 영문을 유지했다.</li>
<li><b>embedding</b>, TCR, HOG, VGG, KNN, SVM, RF와 데이터셋 표기는 원형을 유지했다.</li>
<li>수식은 LaTeX 원문을 노출하지 않고 ASCII/유니코드 표기로 재작성했다.</li>
<li>표의 수치와 원문의 최고값 굵은 표시는 그대로 보존했다.</li>
</ul>
{content.decode_contents()}
<h2 class="section">각주</h2>
<ol class="refs">
<li>HOG 구현: <a href="https://scikit-image.org/docs/dev/auto_examples/features_detection/plot_hog.html">scikit-image HOG example</a>.</li>
<li>MonoDepth2 구현: <a href="https://github.com/nianticlabs/monodepth2">github.com/nianticlabs/monodepth2</a>.</li>
<li>SVM 구현: <a href="https://scikit-learn.org/stable/modules/svm.html">scikit-learn SVM</a>.</li>
<li>Avant 635는 팔레트 적재에도 쓰이는 다목적 로더이므로 텔레스코픽(prismatic) 붐이라는 추가 자유도가 있으나, 토공 장비에서 일반적이지 않아 본 연구에서는 사용하지 않았다.</li>
</ol>
<h2 class="section">참고문헌</h2>
<p class="refs-note">원문 참고문헌 {len(refs)}개를 원문 서지 표기와 제목을 유지해 수록한다.</p>
<ol class="refs">{refs_html}</ol>
<div class="license"><b>저작권 및 라이선스.</b> © 2022 Strokina, Yang, Pajarinen, Serbenyuk, Kämäräinen and Ghabcheloo. 본 논문은 Creative Commons Attribution License(CC BY)에 따라 배포되는 오픈 액세스 논문이다. 원 저자와 저작권자가 표시되고 학술 관행에 따라 원 출판물이 인용되는 경우 다른 포럼에서 사용·배포·복제할 수 있다.</div>
</div></body></html>'''

(ROOT / "translation.html").write_text(html, encoding="utf-8")
print(f"wrote translation.html: {len(html.encode('utf-8'))} bytes; refs={len(refs)}; figures=13; tables={len(content.find_all('table'))}; equations={len(content.select('pre.equation'))}")
