from pathlib import Path
import re, json, html
import markdown
from bs4 import BeautifulSoup
from datetime import date

BASE = Path(__file__).parent
SRC = BASE / 'source'

# Canonical numbering follows active LaTeX environment order.
fig_labels = {
 'fig:fieldtest':1, 'fig:fieldtest_measurement':2, 'fig:simulator_fidelity':3,
 'fig:multiscale':4, 'fig:hd27-D50G200':5, 'fig:trajectories':6,
 'fig:force_velocity':7, 'fig:work':8, 'fig:error_realtimfactor':9,
 'fig:transfer_test_observation':10, 'fig:domain_sensitivity':11,
 'fig:suppl-GD50':12, 'fig:suppl-GD100':13, 'fig:suppl-GD200':14, 'fig:suppl-GD400':15,
}
table_labels = {'table:time_series':1, 'table:field_test':2, 'table:simulators':3,
 'table:sim-to-real_error_granular':4, 'table:sim-to-real_error_terrain':5}
sec_labels = {'sec:sim2realGap':'3절','sec:experiment':'4절','sec:simulator':'5절',
 'sec:particle_terrain':'5.3절','sec:comparison':'6절','sec:supplemental_fig':'부록 보충 그림'}
eq_labels = {'eq:sysID':'식 (1)','eq:momentum':'식 (5)','eq:kinematic_constraint':'식 (6)',
 'eq:limits':'식 (7)','eq:contact_constraint':'식 (8)'}

# Parse canonical bibliography order from the supplied .bbl.
bbl = (SRC/'wl_sim2real_gap.bbl').read_text(errors='ignore')
items = []
for m in re.finditer(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}(.*?)(?=\\bibitem|\\end\{thebibliography\})', bbl, re.S):
    key, body = m.group(1), m.group(2)
    body = re.sub(r'%.*', ' ', body)
    body = re.sub(r'\\(?:newblock|protect|urlprefix)\b', ' ', body)
    body = re.sub(r'\\url\{([^}]*)\}', r'\1', body)
    body = re.sub(r'\\href\{([^}]*)\}\{([^}]*)\}', r'\2 (\1)', body)
    body = re.sub(r'\\(?:em|textit|textbf|mathrm|textrm)\s*\{([^{}]*)\}', r'\1', body)
    body = re.sub(r'[{}~]', ' ', body)
    body = re.sub(r'\\[a-zA-Z]+\*?(?:\[[^]]*\])?', ' ', body)
    body = body.replace('\\&','&').replace('\\%','%').replace('\\_','_')
    body = re.sub(r'\s+', ' ', body).strip(' ,.;') + '.'
    items.append((key, body))
cite_num = {k:i+1 for i,(k,_) in enumerate(items)}

chunks=[]
for i in range(1,10):
    chunks.append((BASE/'fragments'/f'chunk{i:02d}.md').read_text())
text='\n\n'.join(chunks)
# Source bibliography commands are not part of the translated body; references are rebuilt from the canonical .bbl.
text=re.sub(r'(?m)^%?\\+bibliograph(?:y|ystyle)\{[^\n]+$', '', text)

# Correct canonical section headings and a few fragment-local manually inferred references.
repls = {
 '## 서론':'## 1. 서론', '## 관련 연구':'## 2. 관련 연구',
 '## 시뮬레이션과 현실 간 격차 {#sec:sim2realGap}':'## 3. 시뮬레이션과 현실 간 격차',
 '# 4. 실험':'## 4. 실험', '# 5. 시뮬레이터':'## 5. 시뮬레이터',
 '# 6. 비교':'## 6. 비교', '# 7. Force-based control에서의 domain sensitivity와 예측성':'## 7. Force-based control에서의 domain sensitivity와 예측성',
 '## 논의':'## 8. 논의', '## 결론':'## 9. 결론',
 '## 보충 자료':'## 보충 자료', '## 부록 - 보충 그림':'## 부록 — 보충 그림',
 '표 1에 정리했으며':'표 3에 정리했으며', '그림 10에 제시하며':'그림 3에 제시하며',
 '**표 1. 그림 10에 제시한':'**표 3. 그림 3에 제시한', '제5.2절에서 설명':'5.3절에서 설명',
}
for a,b in repls.items(): text=text.replace(a,b)
# Drop duplicated translated title from fragment; cover/front matter supplies it.
text=re.sub(r'^# 변형 가능한 지형을 굴착하는 휠 로더의 시뮬레이션-현실 격차 검토\s*', '', text)

# Cross references before generic TeX cleanup.
def xref(m):
    label=m.group(1)
    if label in fig_labels: return f'<a class="xref" data-source-ref="{label}" href="#fig-{fig_labels[label]}">그림 {fig_labels[label]}</a>'
    if label in table_labels: return f'<a class="xref" data-source-ref="{label}" href="#table-{table_labels[label]}">표 {table_labels[label]}</a>'
    if label in sec_labels: return sec_labels[label]
    if label in eq_labels: return eq_labels[label]
    return label
text=re.sub(r'(?:그림|표)?~?\\+ref\{([^}]+)\}', xref, text)
text=re.sub(r'\\+ref\{([^}]+)\}', xref, text)
text=text.replace('절6절','6절').replace('절5.3절','5.3절')

# Numeric linked citations.
def cite_repl(m):
    keys=[x.strip() for x in m.group(1).split(',') if x.strip()]
    nums=[]
    for k in keys:
        if k not in cite_num: raise ValueError(f'Citation key absent from bbl: {k}')
        nums.append(cite_num[k])
    links=', '.join(f'<a href="#ref-{n}">{n}</a>' for n in nums)
    return f'<span class="citation">[{links}]</span>'
text=re.sub(r'\[\[CITE:([^\]]+)\]\]', cite_repl, text)

# Figure marker -> semantic figure entity. Use canonical crops, not full-page screenshots.
new_lines=[]
for line in text.splitlines():
    if line.startswith('[[FIGURE '):
        lm=re.search(r'label=([^ ]+)',line); cm=re.search(r'caption_ko=(.*)\]\]$',line)
        if not lm or not cm: raise ValueError('Malformed figure marker: '+line[:100])
        label=lm.group(1); cap=cm.group(1); n=fig_labels[label]
        wide = ' fig-wide' if n in {3,5,6,7,8,12,13,14,15} else ''
        new_lines.append(f'<figure id="fig-{n}" data-source-label="{label}" data-figure="{n}" class="paper-figure{wide}">')
        new_lines.append(f'<img src="figures/final/figure-{n:02d}.png" alt="그림 {n}">')
        new_lines.append(f'<figcaption><b>그림 {n}.</b> {cap}</figcaption></figure>')
    else: new_lines.append(line)
text='\n'.join(new_lines)

# TeX display math from translation fragments -> readable Unicode/ASCII pre blocks.
def clean_math(s):
    s=s.strip()
    swaps={'\\boldsymbol{\\theta}':'θ','\\boldsymbol{y}':'y','\\boldsymbol{x}':'x','\\hat{\\boldsymbol{y}}':'ŷ',
           '\\hat{\\boldsymbol{x}}':'x̂','\\mathcal{E}':'E','\\varepsilon':'ε','\\Delta':'Δ','\\phi':'φ',
           '\\arg\\min':'arg min','\\sum':'Σ','\\int':'∫','\\left':'','\\right':'','\\mathrm{d}':'d',
           '\\mathrm{norm}':'norm','\\tag{eq:sysID}':'(1)','\\geq':'≥','\\leq':'≤','\\ldots':'…',
           '\\to':'→','\\mathbb{R}':'R','\\quad':' ','\\,':' '}
    for a,b in swaps.items(): s=s.replace(a,b)
    s=re.sub(r'\\(?:boldsymbol|bm|hat|mathrm|text|mathcal|sc)\{([^{}]*)\}',r'\1',s)
    s=s.replace('\\|','|').replace('\\_','_').replace('\\',' ')
    s=s.replace('{','').replace('}','').replace('^2_W','²_W')
    s=re.sub(r'\s+',' ',s).strip()
    return s

def display_repl(m):
    display_repl.count += 1
    return f'<pre class="equation" data-equation="{display_repl.count}">{html.escape(clean_math(m.group(1)))}</pre>'
display_repl.count=0
text=re.sub(r'\$\$(.*?)\$\$',display_repl,text,flags=re.S)

# Four aligned equations were emitted as explicit Korean equation blocks.
lines=text.splitlines(); out=[]; i=0
while i<len(lines):
    if lines[i].startswith('**(식 ') and 'label:' in lines[i]:
        label=re.search(r'label:\s*([^\)]+)',lines[i]).group(1)
        j=i+1
        while j<len(lines) and not lines[j].strip(): j+=1
        expr=lines[j].strip() if j<len(lines) else ''
        display_repl.count += 1
        no=eq_labels.get(label,f'식 ({display_repl.count})')
        out.append(f'<pre class="equation" id="{label.replace(":","-")}" data-equation="{display_repl.count}">{html.escape(clean_math(expr))}    {no}</pre>')
        i=j+1
    else:
        out.append(lines[i]); i+=1
text='\n'.join(out)

# Inline math -> code, stripping TeX control syntax.
text=re.sub(r'\$([^$\n]+)\$',lambda m:f'<code>{html.escape(clean_math(m.group(1)))}</code>',text)
text=text.replace('\\%','%').replace('\\circ','°').replace('\\textdegree','°')

# Render Markdown (tables preserved as HTML tables).
body_html=markdown.markdown(text,extensions=['tables','sane_lists'])
soup=BeautifulSoup(body_html,'html.parser')
# Canonical heading classes and levels.
for h in soup.find_all(['h1','h2']):
    h.name='h2'; h['class']=['section']
for h in soup.find_all('h3'): h.name='h3'
# Five table entities in source order.
for n,t in enumerate(soup.find_all('table'),1):
    t['id']=f'table-{n}'; t['data-table']=str(n)
    if len(t.find_all('th'))>=6: t['class']=['wide']
    # Convert immediately preceding bold-only paragraph into canonical caption heading.
    prev=t.find_previous_sibling()
    if prev and prev.name=='p' and prev.strong and prev.get_text(strip=True)==prev.strong.get_text(strip=True):
        prev.name='h3'; prev['class']=['table-title']
        txt=prev.get_text(' ',strip=True)
        if not re.match(r'표\s*\d',txt): prev.string=f'표 {n}. {txt}'
        prev['id']=f'table-title-{n}'
# Style the two long error tables as full width with their captions.
for n in (4,5):
    t=soup.find(id=f'table-{n}'); t['class']=['wide','dense']
    p=t.find_previous_sibling();
    if p: p['class']=['table-title','wide-title']

# Remove provenance comments from visible delivery while retaining source IDs as data attributes is not necessary.
for c in soup.find_all(string=lambda x: isinstance(x, type(soup.string)) and False): pass

refs=''.join(f'<li id="ref-{i}">{html.escape(body)}</li>' for i,(k,body) in enumerate(items,1))

css='''
@page { size:A4; margin:14mm 13mm 15mm; }
html{-webkit-print-color-adjust:exact;print-color-adjust:exact} *{box-sizing:border-box}
body{font-family:"Noto Sans CJK KR","Noto Sans KR",Arial,sans-serif;color:#111;font-size:8.7pt;line-height:1.48;margin:0}
.cover{position:relative;height:255mm;padding-left:14mm;page-break-after:always}.cover .bar{position:absolute;left:0;top:0;bottom:0;width:6px;background:#111}.cover .spacer{height:66mm}.cover h1{font-size:27pt;line-height:1.14;margin:0 0 8px;padding-bottom:10px;border-bottom:3px solid #111}.subtitle{font-size:14pt;font-weight:800;margin:10px 0 22px}.meta{font-size:10pt;line-height:1.85}.note{margin-top:18px;color:#666;font-size:8.5pt}
.body{column-count:2;column-gap:7mm;column-fill:auto;text-align:justify}.body p{margin:0 0 6px}.doc-title,h2.section{column-span:all}.doc-title{font-size:16pt;line-height:1.2;border-bottom:2px solid #111;padding-bottom:7px;margin:0 0 7px}h2.section{font-size:14pt;margin:12px 0 7px;padding:5px 0;border-top:1px solid #aaa;border-bottom:1px solid #aaa}h3{font-size:10.5pt;margin:8px 0 4px;break-after:avoid}h3.table-title{font-size:9pt;margin:6px 0 2px}.wide-title{column-span:all}.front{column-span:all;display:grid;grid-template-columns:1fr 1fr;gap:7mm;border-bottom:1px solid #aaa;padding-bottom:7px;margin-bottom:7px}.front ul{margin:2px 0;padding-left:16px}.front li{margin-bottom:3px}
code{font-family:"DejaVu Sans Mono",monospace;font-size:8pt;background:#f2f2f2;padding:0 2px}pre.equation{font-family:"DejaVu Sans Mono",monospace;font-size:7.8pt;white-space:pre-wrap;background:#f5f5f5;border:1px solid #ddd;padding:6px 7px;break-inside:avoid}
figure{margin:7px 0;text-align:center;break-inside:avoid}figure.fig-wide{column-span:all}figure img{max-width:100%;height:auto;max-height:222mm;object-fit:contain}figure[data-figure="12"] img,figure[data-figure="13"] img,figure[data-figure="14"] img,figure[data-figure="15"] img{max-width:82%;max-height:180mm}figcaption{font-size:7.8pt;color:#333;margin-top:3px;text-align:left}.citation{white-space:nowrap}.citation a,.xref{color:#204a76;text-decoration:none}
table{width:100%;border-collapse:collapse;font-size:7.2pt;margin:4px 0 7px;break-inside:avoid}table.wide{column-span:all}th,td{border:.5pt solid #333;padding:2px 3px;text-align:center;overflow-wrap:anywhere}th{background:#e9e9e9;font-weight:700}table.dense{font-size:5.7pt;line-height:1.15}table.dense th,table.dense td{padding:1px 2px;white-space:nowrap}
.references{column-span:all;column-count:2;column-gap:7mm;font-size:6.8pt;line-height:1.3;margin:0;padding-left:18px}.references li{margin-bottom:3px;break-inside:avoid}.refs-note{column-span:all;color:#555}
'''

title='Examining the simulation-to-reality gap of a wheel loader digging in deformable terrain'
front='''<div class="front"><div><b>서지 정보</b><ul>
<li><b>원문 제목</b>: Examining the simulation-to-reality gap of a wheel loader digging in deformable terrain</li>
<li><b>저자</b>: Koji Aoshima, Martin Servin</li><li><b>arXiv</b>: 2310.05765v3 (2024-04-27)</li>
<li><b>원문</b>: <a href="https://arxiv.org/abs/2310.05765">https://arxiv.org/abs/2310.05765</a></li>
</ul></div><div><b>번역 메모</b><ul>
<li><b>wheel loader</b>는 ‘휠 로더’, <b>bucket filling</b>은 ‘버킷 채움’으로 옮긴다.</li>
<li><b>sim-to-real gap</b>, <b>domain sensitivity</b>, <b>control</b>은 의미 구분을 위해 영문 혼합 표기를 유지한다.</li>
<li><b>discrete element method</b>는 첫 등장에 ‘이산요소법(DEM)’으로 표기한다.</li>
<li>수치·단위·변수명·시뮬레이터 충실도 이름(D50–G400)은 원문을 유지한다.</li>
<li>표는 HTML로 재구성하고, 그림은 원문 페이지 전체가 아닌 개별 figure 영역만 사용한다.</li>
</ul></div></div>'''

doc=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{title} — 한국어 전문 번역</title><style>{css}</style></head><body>
<section class="cover"><div class="bar"></div><div class="spacer"></div><h1>{title}</h1><div class="subtitle">한국어 전문 번역</div><div class="meta"><b>저자</b>: Koji Aoshima, Martin Servin<br><b>출처</b>: arXiv:2310.05765v3 · cs.CE / cs.RO<br><b>원문</b>: https://arxiv.org/abs/2310.05765<br><b>번역 생성일</b>: {date.today().isoformat()}</div><div class="note">원문의 섹션 구조와 수치·수식·그림·표를 보존하여 A4 2단 학술 레이아웃으로 재구성한 한국어 완역본이다.</div></section>
<div class="body"><h1 class="doc-title">{title} — 한국어 전체 번역</h1>{front}{str(soup)}
<h2 class="section">참고문헌</h2><p class="refs-note">참고문헌의 논문명·서지 표기는 원문 표기를 유지한다.</p><ol class="references">{refs}</ol></div></body></html>'''
(BASE/'translation.html').write_text(doc)

manifest={
 'figures':[{'no':str(n),'page':p,'desc':d} for n,p,d in [
 (1,5,'현장 시험'),(2,5,'휠 로더 측정량'),(3,7,'8개 시뮬레이터 충실도'),(4,9,'멀티스케일 지형 모델'),(5,10,'HD27 시뮬레이션 연속 장면'),(6,11,'버킷 끝단 trajectory'),(7,13,'속도·힘·회전 시계열'),(8,14,'동력 소비'),(9,14,'오차와 실시간 계수'),(10,15,'control parameter 의존성'),(11,15,'domain sensitivity'),(12,17,'G50/D50 보충 시계열'),(13,18,'G100/D100 보충 시계열'),(14,19,'G200/D200 보충 시계열'),(15,20,'G400/D400 보충 시계열')]],
 'tables':[{'no':str(n),'page':p,'desc':d} for n,p,d in [(1,6,'시계열 측정값'),(2,6,'현장 시험 질량과 일'),(3,6,'시뮬레이터 설정'),(4,10,'D형 오차'),(5,11,'G형 오차')]],
 'display_equations':9
}
(BASE/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(BASE/'citation_map.json').write_text(json.dumps({'citations':[{'key':k,'number':i+1,'text':v} for i,(k,v) in enumerate(items)]},ensure_ascii=False,indent=2))
print(f'HTML built: figures={len(fig_labels)}, tables={len(soup.find_all("table"))}, equations={display_repl.count}, refs={len(items)}')
