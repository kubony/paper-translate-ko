from pathlib import Path
import re, html, json

ROOT=Path(__file__).resolve().parent
F=ROOT/'fragments'
S=ROOT/'source'

def read(name): return (F/name).read_text()

# Active paper order: main body, conclusion, then appendix.
main = '\n\n'.join([read('part1_ko.md'), read('part2_ko.md'), read('part3a_experiment_ko.md')])
ct = read('conclusion_appendix_401_435_ko.md')
conclusion, tail = ct.split('<!-- source: sections/appendix.tex:401-414 -->',1)
app_tables=read('appendix_tables_ko.md')
tab20, rest=app_tables.split('### 표 21.',1)
tab21='### 표 21.'+rest.split('### 표 22.',1)[0]
tab22='### 표 22.'+rest.split('### 표 22.',1)[1].split('### 표 23.',1)[0]
tab23_24='### 표 23.'+rest.split('### 표 23.',1)[1]
app1=read('appendix_001_050_ko.md')
app1=app1.replace('\\input{tables/text-bench-compare}',tab20)
app1=app1.replace('\\input{tables/text-bench-classification}',tab21)
app1=app1.replace('\\input{tables/text-bench-evluation}',tab22)
appendix='\n\n'.join([
 app1,read('appendix_051_100_ko.md'),read('appendix_101_150_ko.md'),
 read('appendix_b_ko.md'),read('appendix_301_350_ko.md'),tab23_24,
 read('appendix_351_400_ko.md'),'<!-- source: sections/appendix.tex:401-414 -->'+tail
])
md='\n\n'.join([main, conclusion, '# 부록\n', appendix])

# Canonical numeric citation order generated with the paper's plain.bst bibliography style.
# Inline citations become compact [1–3, 7] links instead of leaking raw BibTeX keys.
citation_map=json.loads((ROOT/'citation_map.json').read_text())

def compact_ranges(numbers):
    numbers=sorted(set(numbers))
    runs=[]
    start=prev=numbers[0]
    for n in numbers[1:]:
        if n == prev + 1:
            prev=n
            continue
        runs.append((start,prev)); start=prev=n
    runs.append((start,prev))
    return runs

def cite_html(keys):
    nums=[citation_map[k] for k in keys if k in citation_map]
    if not nums:
        return ''
    parts=[]
    for a,b in compact_ranges(nums):
        label=str(a) if a == b else (f'{a}, {b}' if b == a + 1 else f'{a}–{b}')
        parts.append(f'<a href="#ref-{a}">{label}</a>')
    return '<span class="citation">['+', '.join(parts)+']</span>'

def replace_key_brackets(match):
    keys=[k.strip() for k in match.group(1).split(';')]
    return cite_html(keys) if keys and all(k in citation_map for k in keys) else match.group(0)

md=re.sub(r'\[([A-Za-z0-9_.:-]+(?:;\s*[A-Za-z0-9_.:-]+)*)\]', replace_key_brackets, md)
md=re.sub(r'~?\\cite\w*\{([^}]+)\}', lambda m: cite_html([k.strip() for k in m.group(1).split(',')]), md)

# Canonical source-native figures. Figure 19 and Figure 28 are reconstructed prompt blocks.
figmap={
1:'figures/teasers/overview_page1.pdf',2:'figures/teasers/overview_page2.pdf',
3:'figures/method/method-1.pdf',4:'figures/method/method-2.pdf',
19:'figures/generated/figure19_prompt.png'}
for n,path in figmap.items():
    # Insert after the first caption line for this number.
    pat=re.compile(rf'(^\*\*그림 {n}\..*?$)',re.M)
    md=pat.sub(rf'\1\n\n<figure data-figure="{n}"><img src="source/{path}" alt="그림 {n}"></figure>',md,count=1)
# Data/experiment source path markers with canonical figure IDs.
figure_no_by_path={
 'figures/data/general_data_example.pdf':5,'figures/data/general_data_pipeline.pdf':6,
 'figures/data/text_data_example.pdf':7,'figures/data/text_data_pipeline_render.pdf':8,
 'figures/data/text_data_pipeline_edit.pdf':9,'figures/data/science_data_pipeline.pdf':10,
 'figures/data/science_data_example.pdf':11,'figures/data/spatial_data_example.pdf':12,
 'figures/data/rotation_data_pipeline.pdf':13,'figures/data/humor_data_example.pdf':14,
 'figures/data/humor_data_pipeline.pdf':15,'figures/data/cot_general_example.pdf':16,
 'figures/data/cot_knowledge_example.pdf':17,'figures/data/cot_science_example.pdf':18,
 'figures/experiment/gen_general_data_comp.pdf':20,'figures/experiment/gen_text_data_comp.pdf':21,
 'figures/experiment/gen_knowledge_data_comp.pdf':22,'figures/experiment/edit_general_data_comp.pdf':23,
 'figures/experiment/edit_text_data_comp.pdf':24,'figures/experiment/edit_cot_data_comp.pdf':25,
 'figures/experiment/edit_more_data_comp.pdf':26,
}
def source_figure(match):
    path=match.group(1)
    no=figure_no_by_path.get(path)
    if no is None:
        raise ValueError(f'unmapped source figure path: {path}')
    return f'<figure data-figure="{no}"><img src="source/{path}" alt="그림 {no}"></figure>'
md=re.sub(r'\[그림: `([^`]+\.pdf)`\]\s*<span[^>]*></span>',source_figure,md)
# Appendix source figure environment and markdown image.
md=md.replace('**그림. MLLM 기반 자동 평가에 사용한 시스템 프롬프트 템플릿.**', '**그림 28. MLLM 기반 자동 평가에 사용한 시스템 프롬프트 템플릿.**\n\n<figure data-figure="28"><img src="source/figures/generated/figure28_prompt.png" alt="그림 28"></figure>', 1)
md=re.sub(r'\\begin\{figure\}.*?\\includegraphics\[[^]]*\]\{([^}]+)\}.*?\\caption\{\\textbf\{([^}]*)\}\}.*?\\end\{figure\}',lambda m:f'<figure data-figure="27"><img src="source/{m.group(1)}" alt="그림 27"><figcaption><b>그림 27.</b> {m.group(2)}</figcaption></figure>',md,flags=re.S)
md=re.sub(r'!\[([^]]*)\]\((figures/[^)]+\.pdf)\)',lambda m:f'<figure data-figure="29"><img src="source/{m.group(2)}" alt="{m.group(1)}"></figure>',md)

# Remove layout-only LaTeX and normalize cross references/citations.
md=re.sub(r'^\\(?:label|vspace|noindent|centering)\{?[^\n]*$', '', md, flags=re.M)
md=re.sub(r'^\\(?:begin|end)\{[^}]+\}[^\n]*$', '', md, flags=re.M)
md=re.sub(r'\\(?:cref|ref)\{([^}]+)\}', lambda m: m.group(1).replace('tab:','표 ').replace('fig:','그림 '), md)
if re.search(r'\\cite\w*\{', md):
    raise ValueError('unmapped citation command remains in merged translation')
md=md.replace('``','“').replace("''",'”')

# Display math -> semantic equation blocks; strip common LaTeX commands but preserve symbols.
def clean_math(x):
    x=x.strip()
    repl={r'\\text':'',r'\\mathbf':'',r'\\mathcal':'',r'\\mathbb':'',r'\\cdot':'·',r'\\times':'×',r'\\frac':'FRAC',r'\\max':'max',r'\\sum':'Σ',r'\\in':'∈',r'\\ge':'≥',r'\\le':'≤'}
    for a,b in repl.items(): x=x.replace(a,b)
    x=re.sub(r'FRAC\{([^{}]+)\}\{([^{}]+)\}',r'(\1)/(\2)',x)
    x=x.replace('\\left','').replace('\\right','').replace('\\,',' ').replace('\\;',' ').replace('\\!','')
    x=x.replace('\\','').replace('{','').replace('}','')
    return x
md=re.sub(r'\$\$(.*?)\$\$',lambda m:f'\n<pre class="equation">{html.escape(clean_math(m.group(1)))}</pre>\n',md,flags=re.S)
# Bold equations emitted by part1.
md=re.sub(r'<!-- equation:[^>]*-->\s*\n\*\*(.*?)\*\*',lambda m:f'<pre class="equation">{html.escape(m.group(1))}</pre>',md)
# Inline math: preserve readable content without raw backslashes.
md=re.sub(r'\$([^$\n]+)\$',lambda m:f'<code>{html.escape(clean_math(m.group(1)))}</code>',md)
# Remove any residual isolated LaTeX commands, preserving human-readable argument text.
md=re.sub(r'\\(?:textbf|textit|emph)\{([^{}]*)\}',r'**\1**',md)
md=re.sub(r'\\[A-Za-z]+\*?(?:\[[^]]*\])?', '', md)

# Bibliography from source BibTeX, ordered exactly like plain.bst and limited to cited works.
bib=(S/'refs.bib').read_text(errors='ignore')
entry_by_key={}
def clean_bib_text(value):
    value=re.sub(r'[{}]','',value).replace('\\&','&').replace('\\mu','μ')
    value=re.sub(r'\\[A-Za-z]+','',value)
    return re.sub(r'\s+',' ',value).strip()
def first_author_label(value):
    first=clean_bib_text(value).split(' and ',1)[0].strip()
    if ',' in first:
        return first.split(',',1)[0].strip()
    words=first.split()
    return words[-1] if words else 'Unknown'
for block in re.split(r'\n@', '\n'+bib)[1:]:
    key=block.split('{',1)[1].split(',',1)[0].strip() if '{' in block else ''
    mt=re.search(r'\btitle\s*=\s*[\{\"](.*?)(?<!\\)[\}\"]\s*,?\s*\n',block,re.S|re.I)
    ma=re.search(r'\bauthor\s*=\s*[\{\"](.*?)(?<!\\)[\}\"]\s*,?\s*\n',block,re.S|re.I)
    my=re.search(r'\byear\s*=\s*[\{\"]?([^,}\"\n]+)',block,re.I)
    if key and mt:
        entry_by_key[key]={
            'author': first_author_label(ma.group(1)) if ma else 'Unknown',
            'multiple_authors': bool(ma and ' and ' in ma.group(1)),
            'year': clean_bib_text(my.group(1)) if my else 'n.d.',
            'title': clean_bib_text(mt.group(1)),
        }
ordered_keys=[k for k,_ in sorted(citation_map.items(),key=lambda kv:kv[1])]
missing=[k for k in ordered_keys if k not in entry_by_key]
if missing:
    raise ValueError(f'cited BibTeX entries missing metadata: {missing}')
ref_items=[]
for key in ordered_keys:
    n=citation_map[key]; e=entry_by_key[key]
    suffix=' et al.' if e['multiple_authors'] else ''
    ref_items.append(f'<li id="ref-{n}"><span class="ref-author">{html.escape(e["author"]+suffix)}</span> ({html.escape(e["year"])}). {html.escape(e["title"])}.</li>')
refs_html='<section class="references"><h1>참고문헌</h1><p>본문에서 인용한 참고문헌 '+str(len(ordered_keys))+'개를 원문의 번호 순서로 정리했다.</p><ol>'+''.join(ref_items)+'</ol></section>'
md += '\n\n'+refs_html+'\n'

# Markdown to HTML.
import markdown
body=markdown.markdown(md,extensions=['extra','tables','fenced_code','sane_lists'])
# Add table wrappers/classes for multicol printing.
body=body.replace('<table>','<div class="table-wrap"><table class="wide">').replace('</table>','</table></div>')

meta=json.loads((ROOT/'metadata.json').read_text())
authors=', '.join(a['name'] for a in meta['authors'])
css=r'''
@page { size:A4; margin:13mm 14mm 15mm; }
*{box-sizing:border-box} body{margin:0;font-family:"Noto Sans CJK KR","Noto Sans KR",Arial,sans-serif;color:#15202b;font-size:8.35pt;line-height:1.52}
.cover{height:245mm;page-break-after:always;display:flex;flex-direction:column;justify-content:center;padding:20mm 16mm;border-left:9px solid #234f8a}.cover h1{font-size:27pt;line-height:1.12;margin:0 0 12mm;border-bottom:3px solid #234f8a;padding-bottom:8mm}.cover .ko{font-size:16pt;font-weight:700;color:#234f8a}.cover .meta{margin-top:16mm;font-size:10pt;line-height:1.8}.cover .note{margin-top:auto;color:#536170;font-size:8.5pt}
.front{page-break-after:always;display:grid;grid-template-columns:1fr 1fr;gap:10mm;padding-top:8mm}.front h2{color:#234f8a}.paper{column-count:2;column-gap:8mm;column-rule:none}.paper h1,.paper h2,.paper .table-wrap,.paper figure{column-span:all}.paper h1{font-size:16pt;color:#173d69;border-top:2px solid #234f8a;border-bottom:.7px solid #9db1c8;padding:4px 0;margin:9mm 0 4mm;break-after:avoid}.paper h2{font-size:12pt;color:#234f8a;margin:6mm 0 2mm}.paper h3{font-size:10pt;color:#315d8f;margin:4mm 0 1.5mm;break-after:avoid}.paper h4{font-size:9pt;margin:3mm 0 1mm;break-after:avoid}.paper p{margin:0 0 2.1mm;text-align:justify;orphans:3;widows:3}.paper li{margin-bottom:1mm}.paper figure{margin:4mm auto 5mm;text-align:center;break-inside:avoid}.paper figure img{max-width:100%;max-height:205mm;object-fit:contain}.paper figcaption{font-size:7.5pt;color:#34495e;text-align:left;margin-top:1.5mm}.table-wrap{margin:4mm 0 6mm;overflow:visible;break-inside:avoid}.wide{column-span:all;border-collapse:collapse;width:100%;font-size:6.5pt;line-height:1.25}.wide th,.wide td{border:.35pt solid #96a5b5;padding:1.1mm 1.2mm;vertical-align:middle}.wide th{background:#e8eef5;font-weight:700}.wide tr:nth-child(even) td{background:#f8fafc}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f4f7fa;border-left:3px solid #6b8db2;padding:2.2mm;font:6.8pt/1.35 "DejaVu Sans Mono",monospace;break-inside:avoid}.equation{column-span:all;text-align:center;background:#f8fafc;border:1px solid #d4dde7;border-left:4px solid #234f8a;font-size:7.5pt}.paper code{font:7.2pt "DejaVu Sans Mono",monospace;background:#f2f4f6;padding:0 .4mm}.paper blockquote{border-left:3px solid #9cb0c5;margin:2mm 0;padding:1mm 3mm;color:#475569}.paper a{color:#1e5c9a;text-decoration:none}.citation{white-space:nowrap;font-size:.88em;color:#315d8f;font-variant-numeric:tabular-nums}.citation a{color:inherit;text-decoration:none}.references ol{padding-left:6mm;margin-top:2mm}.references li{font-size:7.15pt;line-height:1.35;margin:0 0 1.4mm;padding-left:.5mm;break-inside:avoid}.ref-author{font-weight:600}.src{display:none}
'''
cover=f'''<section class="cover"><div class="ko">한국어 전문 번역</div><h1>{html.escape(meta['title'])}</h1><div class="meta"><b>저자:</b> {html.escape(authors)}<br><b>분야:</b> {meta['primary_category']} · Technical Report<br><b>arXiv:</b> {meta['arxiv_id']} (v1)<br><b>원문:</b> {meta['pdf_url']}<br><b>프로젝트:</b> https://github.com/OpenGVLab/InternVL-U<br><b>번역 생성일:</b> 2026-08-03<br><b>작성자:</b> 제니</div><div class="note">초록부터 부록까지 완역하고, 원문 피겨·표·수식 및 2단 학술 레이아웃을 보존했다.</div></section>'''
front=f'''<section class="front"><div><h2>서지 정보</h2><p><b>원제</b><br>{html.escape(meta['title'])}</p><p><b>저자</b><br>{html.escape(authors)}</p><p><b>원문</b><br>{meta['abs_url']}<br>{meta['pdf_url']}</p><p><b>기준</b><br>arXiv v1 · 61 pages · 2026-03-10</p></div><div><h2>번역 메모</h2><ul><li>Unified multimodal model(UMM), MLLM, MMDiT 등 핵심 약어와 모델명은 원문 표기를 유지했다.</li><li>generation, editing, reasoning, policy, action, Flow Matching, CoT 등은 의미 손실을 줄이기 위해 혼합 표기했다.</li><li>표의 모델명·벤치마크명·지표명·수치·단위를 원문 그대로 보존했다.</li><li>디스플레이 수식은 검색 가능한 ASCII/Unicode 표현으로 옮겼다.</li><li>저자의 주장과 번역자의 해석을 섞지 않았으며, 원문에 없는 구현 사실을 추가하지 않았다.</li><li>본문 인용은 원문 참고문헌 순서에 맞춘 압축 숫자형 링크(예: [12–14, 21])로 표기했다.</li></ul></div></section>'''
out='<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>InternVL-U 한국어 전문 번역</title><style>'+css+'</style></head><body>'+cover+front+'<main class="paper">'+body+'</main></body></html>'
(ROOT/'translation.html').write_text(out)
(ROOT/'merged_translation.md').write_text(md)
print('wrote',ROOT/'translation.html','chars',len(out),'bib',len(ordered_keys),'tables',body.count('<table'),'figures',body.count('<figure'),'equations',body.count('class="equation"'))
