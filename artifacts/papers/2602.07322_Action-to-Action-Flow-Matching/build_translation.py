#!/usr/bin/env python3
from pathlib import Path
import json, re, html, unicodedata
import markdown
from bs4 import BeautifulSoup
from pylatexenc.latex2text import LatexNodes2Text
from pybtex.database import parse_file

BASE=Path(__file__).resolve().parent
FRAGS=[BASE/'fragments/part1a.md',BASE/'fragments/part1b.md',BASE/'fragments/part2a.md',BASE/'fragments/part2b.md',BASE/'fragments/part2c.md',BASE/'fragments/part3.md']
MAN=json.loads((BASE/'manifest.json').read_text())
FIG={x['label']:x for x in MAN['figures']}
TAB={x['label']:x for x in MAN['tables']}
EQ={str(x.get('label') or x['no']):x for x in MAN['equations']}
EQ.update({str(x['no']):x for x in MAN['equations']})
SECTION_REFS={'sec-initial_state':('4.3.2','section-4-3-2'),'appen_dr':('A.1','section-a-1'),'appen_param':('A.2','section-a-2'),'appen_video':('A.4','section-a-4')}

# Canonical bibliography order from plainnat-generated .bbl.
bbl=(BASE/'source/minimal.bbl').read_text(errors='replace')
keys=re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',bbl,re.S)
CNUM={k:i+1 for i,k in enumerate(keys)}
assert len(keys)==42 and len(set(keys))==42
bib=parse_file(str(BASE/'source/paper.bib'))
(BASE/'citation_map.json').write_text(json.dumps(CNUM,ensure_ascii=False,indent=2)+'\n')

latex=LatexNodes2Text(math_mode='text')
def tex_text(s):
    s=s.replace('\\m{}','A2A')
    try: s=latex.latex_to_text(s)
    except Exception: pass
    s=unicodedata.normalize('NFKC',s).replace('ẑ','z_hat').replace('∼','~')
    s=s.replace('ℝ&gt;0','ℝ₍&gt;0₎')
    return re.sub(r'\s+',' ',s).strip()

def inline_math(text):
    def repl(m): return '<code>'+html.escape(tex_text(m.group(1)))+'</code>'
    return re.sub(r'(?<!\\)\$([^$\n]+)\$',repl,text)

def citation_html(raw):
    ks=[k.strip() for k in raw.split(',') if k.strip()]
    nums=sorted({CNUM[k] for k in ks})
    parts=[]; i=0
    while i<len(nums):
        j=i
        while j+1<len(nums) and nums[j+1]==nums[j]+1: j+=1
        if j-i>=2:
            parts.append(f'<a href="#ref-{nums[i]}">{nums[i]}–{nums[j]}</a>')
        else:
            parts.extend(f'<a href="#ref-{n}">{n}</a>' for n in nums[i:j+1])
        i=j+1
    return '<span class="citation">['+', '.join(parts)+']</span>'

def xref_html(label):
    if label in FIG:
        n=FIG[label]['no']; return f'<a class="xref" data-source-ref="{html.escape(label)}" href="#fig-{n}">그림 {n}</a>'
    if label in TAB:
        n=TAB[label]['no']; return f'<a class="xref" href="#table-{n}">표 {n}</a>'
    if label in EQ:
        n=EQ[label]['no']; return f'<a class="xref" href="#eq-{n}">식 ({n})</a>'
    if label in SECTION_REFS:
        n,ident=SECTION_REFS[label]; return f'<a class="xref" href="#{ident}">{n}절</a>'
    raise KeyError('unknown XREF '+label)

def md_inline(s):
    s=inline_math(s)
    out=markdown.markdown(s,extensions=[]).strip()
    return out[3:-4] if out.startswith('<p>') and out.endswith('</p>') else out

def figure_replace(m):
    label=m.group(1).strip(); caption=m.group(2).strip(); x=FIG[label]; n=x['no']
    wide=' fig-wide' if x.get('width')=='figure*' or x.get('environment')=='figure*' else ''
    src=x['asset'].replace('source/','source/')
    width_match=re.match(r'([0-9.]+)\\linewidth',str(x.get('width','1\\linewidth')))
    width_pct=max(10,min(100,round(float(width_match.group(1))*100))) if width_match else 100
    return (f'<figure class="paper-figure{wide}" id="fig-{n}" data-source-label="{html.escape(label)}" data-figure="{n}">\n'
            f'<img src="{html.escape(src)}" style="width:{width_pct}%" alt="그림 {n}">\n'
            f'<figcaption><b>그림 {n}.</b> {md_inline(caption)}</figcaption>\n</figure>')

def preprocess(raw):
    raw=raw.replace('\n## 일반화 성능\n\n## 일반화 성능\n','\n## 일반화 성능\n')
    # Remove the split-boundary heading duplicated at the end of part2b.
    raw=raw.replace('\n## 일반화 성능\n\n\n## 일반화 성능\n','\n## 일반화 성능\n')
    raw=re.sub(r'\n## 일반화 성능\s*\Z','\n',raw)
    raw=re.sub(r'\[\[CITE:([^\]]+)\]\]',lambda m:citation_html(m.group(1)),raw)
    raw=re.sub(r'\[\[XREF:([^\]]+)\]\]',lambda m:xref_html(m.group(1).strip()),raw)
    # Figure marker plus its one-paragraph caption.
    raw=re.sub(r'\[\[FIGURE:([^\]]+)\]\]\s*\n+([^\n].*?)(?=\n\s*\n|\Z)',figure_replace,raw,flags=re.S)
    # Equations: exactly one $$ block after each marker.
    def eqrepl(m):
        label=m.group(1).strip(); body=m.group(2).strip(); x=EQ[label]; n=x['no']
        return f'<pre class="equation" id="eq-{n}" data-equation="{n}">{html.escape(tex_text(body))}    ({n})</pre>'
    raw=re.sub(r'\[\[EQUATION:([^\]]+)\]\]\s*\n+\$\$(.*?)\$\$',eqrepl,raw,flags=re.S)
    # Table markers survive Markdown and are associated with the next table in DOM.
    raw=re.sub(r'\[\[TABLE:([^\]]+)\]\]',lambda m:f'<div class="table-marker" data-table-label="{html.escape(m.group(1).strip())}"></div>',raw)
    raw=inline_math(raw)
    return raw

pieces=[]
for p in FRAGS:
    s=p.read_text()
    if p.name=='part3.md':
        # The split overlaps the pre-section Figure 11 already translated at the end of part2c.
        s=re.sub(r'^\[\[FIGURE:video_generation\]\]\s*\n+.*?(?=\n\s*\n# Video generation에의 적용)', '', s, flags=re.S)
    pieces.append(s)
raw='\n\n'.join(pieces)
raw=preprocess(raw)
body=markdown.markdown(raw,extensions=['tables','fenced_code','footnotes'])
soup=BeautifulSoup(body,'html.parser')
# Associate each marker with its next table and add canonical title.
for marker in list(soup.select('div.table-marker')):
    label=marker.get('data-table-label'); x=TAB[label]; n=x['no']; table=marker.find_next('table')
    if table is None: raise RuntimeError('no table after '+label)
    table['id']=f'table-{n}'; table['data-table']=n
    if len(table.find_all('th'))>=6: table['class']=(table.get('class') or [])+['wide']
    heading=soup.new_tag('h3',attrs={'class':'section table-title'}); heading.string=f'표 {n}. '
    marker.insert_before(heading); marker.decompose()
# Normalize headings and canonical numbers/IDs.
heading_map={
'초록':('초록',True,'abstract'),'서론':('1. 서론',True,'section-1'),'관련 연구':('2. 관련 연구',True,'section-2'),
'Visuomotor policy':('2.1 Visuomotor policy',False,'section-2-1'),'Diffusion의 noise 최적화':('2.2 Diffusion의 noise 최적화',False,'section-2-2'),
'Action-to-action flow matching':('3. Action-to-Action Flow Matching',True,'section-3'),'Flow matching':('3.1 Flow matching',False,'section-3-1'),'Action to action flow':('3.2 Action-to-Action flow',False,'section-3-2'),'Learning objectives':('3.3 학습 objective',False,'section-3-3'),
'평가':('4. 평가',True,'section-4'),'훈련 효율성':('4.1 훈련 효율성',False,'section-4-1'),'추론 비용':('4.2 추론 비용',False,'section-4-2'),'일반화 성능':('4.3 일반화 성능',False,'section-4-3'),'시각적 불확실성':('4.3.1 시각적 불확실성',False,'section-4-3-1'),'초기 상태 불확실성':('4.3.2 초기 상태 불확실성',False,'section-4-3-2'),
'Ablation study':('5. Ablation study',True,'section-5'),'Regression 또는 생성':('5.1 Regression 또는 생성',False,'section-5-1'),'Action space 또는 latent space':('5.2 Action space 또는 latent space',False,'section-5-2'),
'Video generation에의 적용':('6. Video generation에의 적용',True,'section-6'),'결론':('7. 결론',True,'section-7'),'한계':('8. 한계',True,'section-8'),'부록':('부록 A',True,'section-a'),
'Randomization level 설정':('A.1 Randomization level 설정',False,'section-a-1'),'Hyperparameter':('A.2 Hyperparameter',False,'section-a-2'),'Experimental setup':('A.3 Experimental setup',False,'section-a-3'),'Video generation':('A.4 Video generation',False,'section-a-4')}
# First title heading is redundant.
first=soup.find(['h1','h2'],string=lambda s:s and s.strip()=='Action-to-Action Flow Matching')
if first: first.decompose()
for h in soup.find_all(re.compile('^h[1-6]$')):
    text=h.get_text(' ',strip=True)
    if text in heading_map:
        new,full,ident=heading_map[text]; h.name='h2' if full else 'h3'; h.string=new; h['id']=ident
        if full: h['class']=(h.get('class') or [])+['section']
# Remove any duplicate 4.3 heading produced at fragment boundary.
seen=False
for h in list(soup.find_all(id='section-4-3')):
    if seen: h.decompose()
    seen=True

# References in canonical plainnat order.
def clean_bib_text(s): return tex_text(s).replace(' et al.',' et al.')
refs=[]
for k in keys:
    e=bib.entries[k]; person=e.persons.get('author',[None])[0]
    surname=' '.join(person.last_names) if person else k
    year=e.fields.get('year','n.d.'); title=clean_bib_text(e.fields.get('title','제목 없음'))
    refs.append(f'<li id="ref-{CNUM[k]}">{html.escape(surname)} et al. ({html.escape(year)}). {html.escape(title)}.</li>')
refs_html='<h2 class="section" id="references">참고문헌</h2><ol class="references">'+''.join(refs)+'</ol>'

# Project-page video appendix.
video_data=json.loads((BASE/'assets/videos.json').read_text())
vids=[x for x in video_data['assets'] if x.get('kind')=='video']
title_map={'new-vedio':'A2A 프로젝트 소개','A2A-':'A2A real-world 실행','DDPM-UNet':'DDPM-UNet real-world 실행','FM-UNet':'FM-UNet real-world 실행','L0-':'Simulation Level 0','L1-':'Simulation Level 1','L2-':'Simulation Level 2','L3-':'Simulation Level 3','pick_cube_new_target':'Pick Cube — 새로운 target','pick_cube-':'Pick Cube real-world 실행','6-':'초기 상태 실험 #6','13-':'초기 상태 실험 #13','15-':'초기 상태 실험 #15'}
cards=[]
for i,v in enumerate(vids,1):
    local=v['local']; stem=Path(local).stem; title=next((val for key,val in title_map.items() if key in stem),stem)
    thumb='assets/videos/thumbs/'+Path(local).stem+'.jpg'
    cards.append(f'<figure class="video-card"><a href="{html.escape(local)}"><img src="{html.escape(thumb)}" alt="영상 {i}"></a><figcaption><b>영상 {i}.</b> {html.escape(title)}. <span class="video-links">▶ <a href="{html.escape(local)}">레포 사본</a> · <a href="{html.escape(v["url"])}">원본</a></span></figcaption></figure>')
video_html='<h2 class="section" id="video-assets">프로젝트 페이지 영상 자산</h2><p>공식 프로젝트 페이지의 영상 13개를 원본 URL과 함께 보존했다.</p><div class="video-grid">'+''.join(cards)+'</div>'

css='''
@page { size:A4; margin:15mm; }
html {-webkit-print-color-adjust:exact;print-color-adjust:exact}*{box-sizing:border-box}
body{font-family:"Noto Sans KR","Apple SD Gothic Neo",sans-serif;color:#111;font-size:9.1pt;line-height:1.52;margin:0}
a{color:#164f87;text-decoration:none}.cover{position:relative;min-height:245mm;padding-left:14mm;page-break-after:always}.cover .bar{position:absolute;left:0;top:0;bottom:0;width:6px;background:#111}.cover .spacer{height:56mm}.cover h1{font-size:27pt;line-height:1.14;margin:0 0 7px;padding-bottom:11px;border-bottom:3px solid #111}.cover .subtitle{font-size:14pt;font-weight:800;margin:10px 0 20px}.cover .meta{font-size:9.7pt;line-height:1.8}.cover .note{margin-top:18px;color:#666}.body{column-count:2;column-gap:7mm;column-fill:auto;text-align:justify}.body p{margin:0 0 7px}h1.doc-title,h2.section,h3.section{column-span:all}h1.doc-title{font-size:17pt;border-bottom:2px solid #111;padding-bottom:8px}h2.section{font-size:13.5pt;margin:14px 0 8px;padding:5px 0;border-top:1px solid #aaa;border-bottom:1px solid #aaa}h3{font-size:10.7pt;margin:10px 0 4px;break-after:avoid}.front-grid{column-span:all;display:grid;grid-template-columns:1fr 1fr;gap:8mm;text-align:left;border-bottom:1px solid #ccc;padding-bottom:8px}.front-grid ul{margin:2px 0;padding-left:16px}.front-grid li{margin-bottom:3px}code{font-family:"DejaVu Sans Mono",monospace;font-size:8.3pt;background:#f1f1f1;padding:0 2px}pre.equation{font-family:"DejaVu Sans Mono",monospace;font-size:7.7pt;line-height:1.38;white-space:pre-wrap;word-break:break-word;background:#f5f5f5;border:1px solid #ddd;padding:7px;break-inside:avoid}figure{margin:8px 0;text-align:center;break-inside:avoid}figure.fig-wide{column-span:all}figure img{max-width:100%;height:auto;max-height:220mm;object-fit:contain}figcaption{font-size:8.2pt;color:#444;margin-top:4px;text-align:justify}table{width:100%;border-collapse:collapse;font-size:7.5pt;margin:6px 0;break-inside:avoid}table.wide{column-span:all}th,td{border:.6pt solid #222;padding:3px;text-align:center;vertical-align:middle;overflow-wrap:anywhere}th{background:#e8e8e8}ol.references{margin:0;padding-left:18px;font-size:7.8pt;line-height:1.34}ol.references li{margin-bottom:3px;break-inside:avoid}.citation{white-space:nowrap}.video-grid{column-span:all;display:grid;grid-template-columns:repeat(4,1fr);gap:5px}.video-card{border:1px solid #ddd;padding:3px;margin:0}.video-card img{width:100%;height:24mm;object-fit:contain;background:#111}.video-card figcaption{font-size:7pt;line-height:1.2}.video-links{white-space:nowrap;font-size:6pt}.footnote{font-size:8pt}blockquote{margin:4px 0 8px 12px;color:#444}
'''
title='Action-to-Action Flow Matching'
authors='Jindou Jia, Gen Li, Xiangyu Chen, Tuo An, Yuxuan Hu, Jingliang Li, Xinying Guo, Jianfei Yang'
front=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{title} — 한국어 전문 번역</title><style>{css}</style></head><body>
<section class="cover"><div class="bar"></div><div class="spacer"></div><h1>{title}</h1><div class="subtitle">한국어 전문 번역</div><div class="meta"><div><b>저자</b>: {authors}</div><div><b>소속</b>: MARS Lab, Nanyang Technological University</div><div><b>arXiv</b>: 2602.07322v2 · cs.RO / cs.AI</div><div><b>원문</b>: <a href="https://arxiv.org/abs/2602.07322">https://arxiv.org/abs/2602.07322</a></div><div><b>프로젝트</b>: <a href="https://lorenzo-0-0.github.io/A2A_Flow_Matching/">A2A Flow Matching</a></div><div><b>번역 생성일</b>: 2026-08-11</div><div><b>번역·편집</b>: 제니</div></div><div class="note">초록부터 부록까지 전문을 문어체로 완역하고, 원문 figure 19개·table 3개·display equation 6개와 공식 프로젝트 영상 13개를 보존했다.</div></section>
<div class="body"><h1 class="doc-title">{title} — 한국어 전체 번역</h1><div class="front-grid"><div><b>서지 정보</b><ul><li>원문 버전: arXiv v2, 2026-05-07</li><li>원문 PDF: <a href="https://arxiv.org/pdf/2602.07322v2">PDF</a></li><li>20쪽, figure 19개</li><li>번역·편집자: 제니</li></ul></div><div><b>번역 메모</b><ul><li>policy, action, flow matching, trajectory는 robotics 의미를 보존해 혼합 표기한다.</li><li>proprioceptive action은 proprioceptive action/고유수용성 action으로 문맥에 맞춰 쓴다.</li><li>latent space, source/target distribution, inference step은 원형을 유지한다.</li><li>모델명·데이터셋명·metric·수치·변수는 원문 표기를 보존한다.</li><li>display equation은 Unicode/ASCII 기반으로 재작성했다.</li><li>표는 이미지가 아니라 HTML table로 재구성했다.</li></ul></div></div>'''
final=front+str(soup)+refs_html+video_html+'</div></body></html>'
(BASE/'translation.html').write_text(final)
# Structural invariants.
fs=BeautifulSoup(final,'html.parser')
assert {x.get('data-figure') for x in fs.select('[data-figure]')}=={str(x['no']) for x in MAN['figures']}
assert {x.get('data-table') for x in fs.select('table[data-table]')}=={str(x['no']) for x in MAN['tables']}
assert [x.get('data-equation') for x in fs.select('pre.equation')]==[str(i) for i in range(1,7)]
assert len(fs.select('ol.references > li'))==42
assert len(fs.select('figure.video-card'))==13
visible=fs.get_text(' ')
for bad in ['[[FIGURE:','[[TABLE:','[[EQUATION:','[[XREF:','[[CITE:','$$','\\begin{','\\frac','\\mathbf','\\mathcal']:
    assert bad not in final, bad
print('wrote',BASE/'translation.html','chars',len(final),'figures',len(fs.select('[data-figure]')),'tables',len(fs.select('table[data-table]')),'equations',len(fs.select('pre.equation')),'refs',len(fs.select('ol.references > li')),'videos',len(fs.select('figure.video-card')))
