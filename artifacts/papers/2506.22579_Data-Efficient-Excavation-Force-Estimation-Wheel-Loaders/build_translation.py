#!/usr/bin/env python3
from pathlib import Path
import re, html, json
import markdown
from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parent
P1 = (ROOT/'fragments/part1_ko.md').read_text()
P2 = (ROOT/'fragments/part2_ko.md').read_text()
P3 = (ROOT/'fragments/part3_ko.md').read_text()

# Resolve fragment boundaries from the original two-column source.
p1_lines = P1.splitlines()
p2_lines = P2.splitlines()
p3_lines = P3.splitlines()
body1 = '\n'.join(p1_lines[14:247])
transition = '''
이 기준선은 8개 토양 parameter를 모두 동시에 추정하는 단일 단계 최적화로 구성되며, 다단계 정식화를 평가하기 위한 기준으로 사용된다. 문제는 constrained nonlinear least-squares optimization으로 정식화하고 유계 제약조건을 처리할 수 있는 gradient-based algorithm L-BFGS-B [35]로 해결한다. 모델이 non-convex이므로 최적화는 초기 parameter 값에 민감하며 local minimum으로 수렴할 수 있다. 이를 완화하기 위해 warm-starting, randomized initialization, multiple starting point를 포함한 여러 전략을 시험하였다.
'''
body2 = '\n'.join(p2_lines[2:])  # skip duplicate III heading
body3 = '\n'.join(p3_lines[2:])  # continue IV-B without duplicate heading
md = body1 + '\n' + transition + '\n' + body2 + '\n' + body3

GREEK = {
    'gamma':'γ','phi':'φ','delta':'δ','alpha':'α','beta':'β','theta':'θ','lambda':'λ',
    'rho':'ρ','pi':'π','varepsilon':'ε','epsilon':'ε','sigma':'σ','mu':'μ'
}

def latex_plain(s: str) -> str:
    s = s.replace('\\begin{aligned}','').replace('\\end{aligned}','')
    s = s.replace('\\quad','  ').replace('\\qquad','    ').replace('\\;',' ')
    s = s.replace('\\left','').replace('\\right','')
    s = re.sub(r'\\tag\{([^{}]+)\}', r'  (\1)', s)
    s = re.sub(r'\\text\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\mathrm\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\boldsymbol\{([^{}]*)\}', r'\1', s)
    s = re.sub(r'\\mathbf\{([^{}]*)\}', r'\1', s)
    # Repeatedly simplify non-nested fractions.
    for _ in range(5):
        ns = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'(\1)/(\2)', s)
        if ns == s: break
        s = ns
    repl = {
        '\\sum':'Σ','\\min':'min','\\max':'max','\\sqrt':'√','\\leq':'≤','\\geq':'≥',
        '\\neq':'≠','\\in':'∈','\\times':'×','\\cdot':'·','\\ldots':'…','\\infty':'∞',
        '\\sin':'sin','\\cos':'cos','\\tan':'tan','\\cot':'cot'
    }
    for k,v in repl.items(): s=s.replace(k,v)
    for k,v in GREEK.items(): s=s.replace('\\'+k,v)
    s = s.replace('\\,',' ').replace('\\!','').replace('\\&','&')
    s = s.replace('\\\\','\n')
    s = re.sub(r'\^\{([^{}]+)\}', r'^(\1)', s)
    s = re.sub(r'_\{([^{}]+)\}', r'_(\1)', s)
    s = re.sub(r'\{([^{}]+)\}', r'\1', s)
    s = s.replace('&=','=').replace('&&','')
    s = re.sub(r'\\[A-Za-z]+', '', s)
    s = s.replace('\\','')
    s = re.sub(r'[ \t]+\n','\n',s)
    s = re.sub(r'\n{3,}','\n\n',s)
    return s.strip()

# Convert display LaTeX into canonical equation code blocks.
md = re.sub(r'\$\$(.*?)\$\$', lambda m: '\n```text\n'+latex_plain(m.group(1))+'\n```\n', md, flags=re.S)
# Convert inline LaTeX to readable monospace text.
md = re.sub(r'\$([^$\n]+)\$', lambda m: '`'+latex_plain(m.group(1))+'`', md)
# Normalize section labels and source naming.
md = md.replace('# III. PARAMETER OPTIMIZATION 방법', '# III. Parameter Optimization 방법')
md = md.replace('Fig. ', '그림 ').replace('Table ', '표 ').replace('Section II', 'II절').replace('Section III', 'III절').replace('Section IV', 'IV절').replace('Section V', 'V절')
# Strip bracket wrappers around Table 1 and normalize entity caption markers.
md = md.replace('[TABLE 1.', '### 표 1.').replace('\n]\n', '\n', 1)
md = re.sub(r'^\[FIGURE (\d+)\.\s*(.*?)\]$', r'**그림 \1.** \2', md, flags=re.M)
md = re.sub(r'^\*\*\[그림 (\d+)\]\*\*\s*(.*)$', r'**그림 \1.** \2', md, flags=re.M)
md = re.sub(r'^\*\*\[표 ([A-Z]?\d+)\]\s*(.*?)\*\*', r'**표 \1. \2**', md, flags=re.M)

body_html = markdown.markdown(md, extensions=['tables','fenced_code','sane_lists'])
soup = BeautifulSoup(body_html, 'html.parser')

# Major headings span both columns.
for h in list(soup.find_all(['h1','h2'])):
    txt = h.get_text(' ', strip=True)
    if h.name == 'h1' or re.match(r'^(초록|I\.|II\.|III\.|IV\.|V\.|감사의 글|부록|참고문헌|저자 약력)', txt):
        h.name='h2'; h['class']=['section']

# Tables: six or more columns must span both columns; place caption with the same context.
for table in soup.find_all('table'):
    cols = len(table.find('tr').find_all(['th','td'])) if table.find('tr') else 0
    if cols >= 6: table['class'] = list(set(table.get('class',[])+['wide']))
    # Left-align descriptive first column.
    for tr in table.find_all('tr'):
        cell=tr.find(['th','td'])
        if cell: cell['class']=list(set(cell.get('class',[])+['l']))

FIGS = {
  1: ('figures_clean/fig-01.png', False),
  2: ('figures_clean/fig-02.png', False),
  3: ('figures_clean/fig-03.png', False),
  4: ('figures_clean/fig-04.png', True),
  5: ('figures_clean/fig-05.png', False),
  6: ('figures_clean/fig-06.png', True),
  7: ('figures_clean/fig-07.png', False),
  8: ('figures_clean/fig-08.png', True),
  9: ('figures_clean/fig-09.png', True),
 10: ('figures_clean/fig-10.png', True),
}
seen=set()
for p in list(soup.find_all('p')):
    txt = p.get_text(' ', strip=True)
    m = re.match(r'^그림\s+(\d+)\.\s*(.*)', txt)
    if not m: continue
    n=int(m.group(1))
    if n not in FIGS or n in seen: continue
    seen.add(n)
    path,wide=FIGS[n]
    fig=soup.new_tag('figure')
    fig['id']=f'fig-{n}'; fig['data-figure']=str(n)
    if wide: fig['class']=['fig-wide']
    img=soup.new_tag('img',src=path,alt=f'그림 {n}')
    cap=soup.new_tag('figcaption')
    b=soup.new_tag('b'); b.string=f'그림 {n}. '
    cap.append(b); cap.append(m.group(2))
    fig.append(img); fig.append(cap)
    p.replace_with(fig)

missing=sorted(set(FIGS)-seen)
if missing: raise SystemExit(f'missing figure captions: {missing}')

# Give equation blocks an explicit class for exact structural assertions.
for pre in soup.find_all('pre'):
    pre['class']=list(set(pre.get('class',[])+['equation']))
# Remove any accidental empty paragraphs.
for p in list(soup.find_all('p')):
    if not p.get_text(strip=True) and not p.find('img'): p.decompose()

# Template CSS (stable prefix from canonical template).
template=(ROOT.parents[2]/'assets/template.html').read_text()
style=re.search(r'<style>(.*?)</style>',template,re.S).group(1)
style += '''
  .body { column-fill: auto; }
  h3.section, .table-caption { column-span: all; }
  table.wide { font-size: 6.9pt; line-height: 1.15; }
  table.wide th, table.wide td { padding: 2px 3px; }
  .source-note { column-span: all; background:#f2f6fa; border-left:3px solid #315f86; padding:8px 10px; margin:8px 0 12px; }
  a { color:#1a4d8f; text-decoration:none; }
'''

meta='''
<h1 class="doc-title">Data-Efficient Excavation Force Estimation for Wheel Loaders — 한국어 전문 번역</h1>
<ul class="biblist">
<li><b>원문 제목</b>: Data-Efficient Excavation Force Estimation for Wheel Loaders</li>
<li><b>저자</b>: Armin Abdolmohammadi, Navid Mojahed, Shima Nazari, Bahram Ravani — University of California, Davis</li>
<li><b>저널</b>: IEEE Access, vol. 13, pp. 181846–181862, 2025</li>
<li><b>DOI</b>: <a href="https://doi.org/10.1109/ACCESS.2025.3622535">10.1109/ACCESS.2025.3622535</a></li>
<li><b>IEEE 문서</b>: <a href="https://ieeexplore.ieee.org/document/11205828">11205828</a></li>
<li><b>arXiv</b>: <a href="https://arxiv.org/abs/2506.22579v2">2506.22579v2</a> · <a href="https://arxiv.org/pdf/2506.22579v2">PDF</a></li>
<li><b>번역 기준</b>: IEEE Access 최종본과 arXiv v2를 대조하였다.</li>
</ul>
<div class="memo-title">번역 메모</div>
<ul class="memo">
<li><b>excavation force</b>는 문맥에 따라 ‘굴착력’ 또는 힘 성분의 ‘굴착 힘’으로 옮긴다.</li>
<li><b>Fundamental Earthmoving Equation(FEE)</b>은 약어와 영문명을 유지한다.</li>
<li><b>soil–tool interaction, stockpile, failure surface, bearing capacity factor</b> 등은 의미 손실을 피하기 위해 혼합 표기한다.</li>
<li>힘 성분, 토양 parameter, 변수, 단위, RMSE 및 식 번호는 원문 표기를 보존한다.</li>
<li>표는 이미지가 아니라 검색·선택 가능한 HTML 표로 재구성한다.</li>
<li>참고문헌 제목과 서지 정보는 원문 언어를 유지한다.</li>
</ul>
<div class="source-note"><b>번역 범위.</b> 초록, 본문 I–V, 감사의 글, 부록 A, 표 1–4·A1–A2, 그림 1–10 캡션, 참고문헌 1–51, 저자 약력 4개를 포함한 완역이다.</div>
'''
cover='''
<section class="cover"><div class="bar"></div><div class="spacer"></div>
<h1>Data-Efficient Excavation Force Estimation for Wheel Loaders</h1>
<div class="subtitle">한국어 전문 번역</div>
<div class="meta">
<div><b>저자</b>: Armin Abdolmohammadi · Navid Mojahed · Shima Nazari · Bahram Ravani</div>
<div><b>저널</b>: IEEE Access 13 (2025), 181846–181862</div>
<div><b>DOI</b>: 10.1109/ACCESS.2025.3622535 &nbsp;|&nbsp; <b>IEEE</b>: 11205828</div>
<div><b>arXiv</b>: 2506.22579v2</div>
<div><b>번역 생성일</b>: 2026-08-11</div>
</div><div class="note">원문 논문의 정보 구조를 보존해 A4 2단 레이아웃으로 재구성했으며, 원문 그림은 개별 자산으로 삽입하고 표는 검색 가능한 HTML 표로 재작성하였다.</div></section>
'''
out=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>휠 로더를 위한 데이터 효율적 굴착력 추정 — 한국어 전문 번역</title><style>{style}</style></head><body>{cover}<div class="body">{meta}{str(soup)}</div></body></html>'''
(ROOT/'translation.html').write_text(out)

manifest={
 'figures':[{'no':str(i),'page':p,'desc':d} for i,p,d in [
 (1,2,'제안 프레임워크 개요'),(2,3,'토양 쐐기 자유물체도'),(3,4,'버킷 적재 힘'),(4,6,'다단계 parameter 추정'),(5,7,'EVERUN ER12 디지털 트윈'),(6,7,'단일/다단계 힘 예측'),(7,8,'다단계 최적화 결과'),(8,9,'다중 경로 비교'),(9,10,'이중 사이클 굴착'),(10,11,'토양 유형별 합력 비교')]],
 'tables':[{'no':n,'page':p,'desc':d} for n,p,d in [('1',3,'기호·parameter·변수'),('2',7,'Algoryx 토양 특성'),('3',8,'최적화 방법 비교'),('4',9,'토양별 parameter'),('A1',14,'문헌 토양 parameter'),('A2',15,'압력–침하 parameter')]],
 'display_equations':28
}
(ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print('wrote',ROOT/'translation.html','figures',len(seen),'tables',len(soup.find_all('table')),'equation blocks',len(soup.find_all('pre')))
