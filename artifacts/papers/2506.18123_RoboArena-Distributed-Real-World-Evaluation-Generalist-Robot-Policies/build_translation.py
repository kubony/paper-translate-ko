#!/usr/bin/env python3
from pathlib import Path
import re, shutil

D = Path(__file__).resolve().parent
TEMPLATE = Path('/home/inkeun/.hermes/skills/research/paper-translate-ko/assets/template.html')
TITLE = 'RoboArena: Distributed Real-World Evaluation of Generalist Robot Policies'
AUTHORS = ('Pranav Atreya, Karl Pertsch, Tony Lee, Moo Jin Kim, Arhan Jain, Artur Kuramshin, '
           'Clemens Eppner, Cyrus Neary, Edward Hu, Fabio Ramos, Jonathan Tremblay, Kanav Arora, '
           'Kirsty Ellis, Luca Macesanu, Marcel Torne Villasevil, Matthew Leonard, Meedeum Cho, '
           'Ozgur Aslan, Shivin Dass, Jie Wang, William Reger, Xingfang Yuan, Xuning Yang, '
           'Abhishek Gupta, Dinesh Jayaraman, Glen Berseth, Kostas Daniilidis, Roberto Martin-Martin, '
           'Youngwoon Lee, Percy Liang, Chelsea Finn, Sergey Levine')

style = re.search(r'<style>(.*?)</style>', TEMPLATE.read_text(), re.S).group(1)
style += r'''
  .cover .authors { font-size: 8.2pt; line-height: 1.45; max-width: 165mm; }
  .body section { break-inside: auto; }
  .body h2:not(.section) { column-span: all; font-size: 15pt; margin: 14px 0 8px; padding: 6px 0; border-top: 1px solid #bbb; border-bottom: 1px solid #bbb; }
  .body ul, .body ol { margin: 4px 0 7px; padding-left: 18px; }
  .body li { margin-bottom: 2px; }
  .equation-inline { text-align: center; margin: 6px 0; }
  .algorithm { border-left: 3px solid #555; background: #f7f7f7; padding: 7px 9px; margin: 8px 0; }
  .metric-card { max-width: 75mm; margin-left: auto; margin-right: auto; }
  .policy-report, .prompt-template { text-align: left; background: #f6f6f6; border: 1px solid #ccc; padding: 9px; }
  figure.text-figure { break-inside: auto; text-align: left; }
  figure.text-figure figcaption { border-top: 1px solid #aaa; padding-top: 4px; }
  ol.references, ol.refs { margin: 0; padding-left: 18px; font-size: 8.2pt; line-height: 1.35; }
  ol.references li, ol.refs li { margin-bottom: 4px; }
  table[data-table="3"] { column-span: all; font-size: 8pt; }
  a { color: #174f8a; text-decoration: none; }
'''

p1 = (D / 'translation_part_1.html').read_text()
p2a = (D / 'translation_part_2a.html').read_text()
p2b = (D / 'translation_part_2b.html').read_text()
p3 = (D / 'translation_part_3.html').read_text()

# Fragment wrappers/header are assembly scaffolding, not paper content.
p1 = re.sub(r'^.*?<article lang="ko">\s*<header>.*?</header>', '', p1, count=1, flags=re.S)
p1 = re.sub(r'</article>\s*$', '', p1, count=1, flags=re.S)

# Correct source-native numbering in prose left by split translation.
p2b = p2b.replace('표 A-2의 결과', '표 2의 결과')
p3 = p3.replace('구체적으로 표 1은', '구체적으로 표 3은')

body = '\n'.join([p1, '<h2 class="section">부록</h2>', p2a, p2b, p3])

# Wrap long text-native figures 13–15 so they remain searchable Korean text rather than page screenshots.
for no, cls in [(13, 'policy-report'), (14, 'prompt-template'), (15, 'prompt-template')]:
    pat = rf'(<article class="{cls}">.*?</article>)\s*<!-- FIGURE {no}: (.*?) -->'
    def wrap(m, no=no):
        return (f'<figure class="fig-wide text-figure" data-figure="{no}">\n{m.group(1)}\n'
                f'<figcaption><b>그림 {no}.</b> {m.group(2).strip()}</figcaption>\n</figure>')
    body, count = re.subn(pat, wrap, body, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f'Figure {no} text wrapper not found')

figures = {
    1: ('figures/source-native/roboarena_teaser.png', True),
    2: ('figures/source-native/roboarena_qualitative_analysis_tool.png', False),
    3: ('figures/source-native/droid_setup.png', False),
    4: ('figures/source-native/roboarena_system.png', True),
    5: ('figures/source-native/roboarena_main_results.png', False),
    6: ('figures/source-native/roboarena_ranking_results.png', False),
    7: ('figures/source-native/roboarena_convergence_results.png', False),
    9: ('figures/source-native/roboarena_cat_results.png', False),
    10: ('figures/source-native/instruction_diversity.png', True),
    11: ('figures/source-native/environment-collage.png', True),
    12: ('figures/source-native/strengths_weaknesses.png', True),
}

def render_marker(m):
    no = int(m.group(1))
    caption = m.group(2).strip()
    if no not in figures:
        raise RuntimeError(f'Unexpected or unmapped figure marker: {no}')
    src, wide = figures[no]
    cls = ' class="fig-wide"' if wide else ''
    return (f'<figure{cls} data-figure="{no}">\n'
            f'  <img src="{src}" alt="그림 {no}">\n'
            f'  <figcaption><b>그림 {no}.</b> {caption}</figcaption>\n'
            f'</figure>')

body = re.sub(r'<!-- FIGURE (\d+): (.*?) -->', render_marker, body, flags=re.S)

# Figure 8 is intentionally a searchable HTML metric card.
if 'data-figure="8"' not in body:
    raise RuntimeError('Figure 8 metric card missing')

# Number the three actual paper tables; Figure 8's internal table is not a paper table.
for no in (1, 2, 3):
    pat = rf'<table([^>]*)>\s*(<caption>표 {no}\.)'
    body, count = re.subn(pat, rf'<table data-table="{no}"\1>\n    \2', body, count=1)
    if count != 1:
        raise RuntimeError(f'Table {no} not found')

# Source layout has section-level headings spanning both columns.
body = re.sub(r'<h2(?![^>]*class=)([^>]*)>', r'<h2 class="section"\1>', body)

video = '''
<h2 class="section">부록. 프로젝트 페이지 영상 자산</h2>
<figure class="video-card">
  <a href="assets/videos/sim_eval-fGTRF_dn-c4b42d.mp4">
    <img src="assets/videos/thumbs/sim_eval-fGTRF_dn-c4b42d.jpg" alt="RoboArena 시뮬레이션 평가 영상">
  </a>
  <figcaption><b>영상 1.</b> RoboArena 프로젝트 페이지의 시뮬레이션 평가 예시.
    <span class="video-links"><span class="video-badge">VIDEO</span>
      <a href="assets/videos/sim_eval-fGTRF_dn-c4b42d.mp4">레포 사본</a> ·
      <a href="https://robo-arena.github.io/assets/sim_eval-fGTRF_dn.mp4">원본</a>
    </span>
  </figcaption>
</figure>
'''
body = body.replace('<section id="references">', video + '\n<section id="references">', 1)

cover = f'''
<section class="cover">
  <div class="bar"></div><div class="spacer"></div>
  <h1>{TITLE}</h1>
  <div class="subtitle">한국어 전문 번역</div>
  <div class="meta">
    <div class="authors"><b>저자</b>: {AUTHORS}</div>
    <div><b>학회</b>: CoRL 2025 &nbsp;|&nbsp; <b>arXiv</b>: 2506.18123v2</div>
    <div><b>원문</b>: https://arxiv.org/abs/2506.18123</div>
    <div><b>번역 생성일</b>: 2026-08-02</div>
    <div><b>번역자</b>: 제니</div>
  </div>
  <div class="note">원문 논문의 정보 구조를 보존해 2단 PDF 레이아웃으로 재구성했으며, 원문 피겨는 개별 자산으로 재삽입하고 표는 HTML로 재구성했다.</div>
</section>'''

front = f'''
<h1 class="doc-title">{TITLE} — 한국어 전체 번역</h1>
<ul class="biblist">
  <li><b>원문 제목</b>: {TITLE}</li>
  <li>저자: {AUTHORS}</li>
  <li>학회: CoRL 2025 / arXiv:2506.18123v2</li>
  <li>원문: https://arxiv.org/abs/2506.18123</li>
  <li>PDF: https://arxiv.org/pdf/2506.18123v2</li>
  <li>프로젝트: https://robo-arena.github.io/</li>
  <li>번역 기준: arXiv v2 PDF 및 LaTeX source 확인</li>
  <li>번역자: 제니</li>
</ul>
<div class="memo-title">번역 메모</div>
<ul class="memo">
  <li><b>generalist policy</b>, <b>policy</b>, <b>action</b>은 로보틱스 문맥의 의미를 보존해 혼합 표기했다.</li>
  <li><b>pairwise comparison</b>은 문맥에 따라 쌍별 비교/A·B 비교로 옮겼다.</li>
  <li><b>progress score</b>와 <b>preference feedback</b>의 역할을 구분해 번역했다.</li>
  <li><b>embodiment</b>와 <b>cross-embodiment</b>는 과번역하지 않고 원형을 유지했다.</li>
  <li>모델명·데이터셋명·지표명·수치·변수는 원문 표기를 유지했다.</li>
  <li>display 수식은 ASCII/유니코드 근사 표기로 재작성했고 표는 HTML로 재구성했다.</li>
  <li>본문 인라인 인용 번호는 제거하고 참고문헌 73개는 원문 제목 중심으로 정리했다.</li>
</ul>'''

html = f'''<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8"><title>{TITLE} — 한국어 전문 번역</title><style>{style}</style></head>
<body>{cover}<div class="body">{front}{body}</div></body></html>'''

(D / 'translation.html').write_text(html)
print('wrote', D / 'translation.html')
print('figures', len(re.findall(r'data-figure="', html)))
print('tables', len(re.findall(r'data-table="', html)))
print('equations', len(re.findall(r'<pre class="equation"', html)))
print('references', len(re.findall(r'<li>', re.search(r'<ol class="references">(.*?)</ol>', html, re.S).group(1))))
print('remaining_markers', len(re.findall(r'FIGURE \d+', html)))
