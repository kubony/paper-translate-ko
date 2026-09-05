#!/usr/bin/env python3
from pathlib import Path
import re, html, json
import markdown
from latex2mathml.converter import convert as latex_to_mathml

W = Path(__file__).resolve().parent
parts = [(W/'translations'/f'part{i}.md').read_text() for i in (1,2,3)]

# Remove worker provenance comments; source ranges remain auditable in the fragment files.
parts = [re.sub(r'^<!--.*?-->\s*', '', p, count=1, flags=re.S) for p in parts]

# Normalize source section hierarchy.
parts[1] = re.sub(r'^# (5 |6 )', r'## \1', parts[1], flags=re.M)
parts[1] = re.sub(r'^## (6\.[1-4] )', r'### \1', parts[1], flags=re.M)

# Figure 6 is preserved as the source figure image, not duplicated as an ASCII plot dump.
parts[2] = re.sub(
    r'그림 안의 게임명, 축 눈금 및 범례는 다음과 같다\(Atari 게임명은 원문 그대로 유지하였다\)\.\s*```text.*?```\s*',
    '', parts[2], flags=re.S)

# Split and reconstruct references so citations can be numeric and linked.
p3 = parts[2]
pre_refs, rest = p3.split('## 참고문헌', 1)
refs_blob, appendices = rest.split('## A 하이퍼파라미터', 1)
ref_pat = re.compile(r'^\[([^]]+)\]\s+(.+)$', re.M)
refs = ref_pat.findall(refs_blob)
keys = [k for k,_ in refs]
expected = ['Bel+15','Bro+16','Dua+16','Hee+17','KL02','KB14','Mni+15','Mni+16','Sch+15a','Sch+15b','SL06','TET12','Wan+16','Wil92']
assert keys == expected, (keys, expected)
ref_map = {k:i+1 for i,k in enumerate(keys)}
refs_html = ['<h2 class="section" id="references">참고문헌</h2>', '<ol class="refs">']
for i,(k,txt) in enumerate(refs,1):
    # Reference titles and venue information intentionally remain in their original language.
    refs_html.append(f'<li id="ref-{i}" data-source-key="{html.escape(k)}">{markdown.markdown(txt)}</li>')
refs_html.append('</ol>')
parts[2] = pre_refs + '\n@@REFERENCES@@\n## A 하이퍼파라미터\n' + appendices

# Source image map. All source figures occupy the paper's full text width.
fig_images = {
    1:'figures/figure-01-clipped-surrogate.png', 2:'figures/figure-02-surrogate-interpolation.png',
    3:'figures/figure-03-mujoco-comparison.png', 4:'figures/figure-04-roboschool-learning-curves.png',
    5:'figures/figure-05-humanoid-frames.png', 6:'figures/figure-06-atari-learning-curves.png'
}

def figure_repl(m):
    n = int(m.group(1)); cap = m.group(2).strip()
    return (f'<figure id="fig-{n}" class="fig-wide" data-figure="{n}">'
            f'<img src="{fig_images[n]}" alt="그림 {n}">'
            f'<figcaption><b>그림 {n}.</b> {cap}</figcaption></figure>')

body_md = '\n\n'.join(parts)
body_md = re.sub(r'^\*\*(?:그림|Figure)\s+([1-6]):\*\*\s*(.+)$', figure_repl, body_md, flags=re.M)
# Lines listing graph titles/legends are source-figure transcription notes, not paper prose.
body_md = re.sub(r'^\*\*Figure [34]의 그래프 제목:\*\*.*\n(?:\*\*(?:Legend|축 이름):\*\*.*\n)?', '', body_md, flags=re.M)

# Convert source citation keys to numeric, linked citations while preserving source order.
key_alt = '|'.join(re.escape(k) for k in sorted(keys, key=len, reverse=True))
def cite_group(m):
    content = m.group(1)
    found = re.findall(key_alt, content)
    if not found:
        return m.group(0)
    # Only transform a bracket if all non-separator content consists of known source keys.
    residue = re.sub(key_alt, '', content)
    if residue.strip(' ;,'):
        return m.group(0)
    links = ', '.join(f'<a href="#ref-{ref_map[k]}">{ref_map[k]}</a>' for k in found)
    return f'<span class="citation">[{links}]</span>'
body_md = re.sub(r'\[([^\]\n]+)\]', cite_group, body_md)

# Replace table captions with semantic blocks.
def tablecap(m):
    n=m.group(1); cap=m.group(2).strip()
    return f'<div class="table-caption" id="table-caption-{n}"><b>표 {n}.</b> {cap}</div>'
body_md = re.sub(r'^\*\*(?:표|Table)\s+([1-6]):\*\*\s*(.+)$', tablecap, body_md, flags=re.M)

# Protect and statically convert display/inline LaTeX to native MathML.
math_blocks=[]
def block_math(m):
    tex=m.group(1).strip()
    tag_m=re.search(r'\\tag\{([^}]+)\}', tex)
    assert tag_m, f'numbered equation lacks tag: {tex[:80]}'
    num=tag_m.group(1)
    tex=re.sub(r'\\tag\{[^}]+\}', '', tex).strip()
    mm=latex_to_mathml(tex).replace('display="inline"','display="block"')
    token=f'PPOBLOCKMATH{len(math_blocks):03d}TOKEN'
    math_blocks.append((token, f'<pre class="equation" data-equation="{num}"><span class="math-wrap">{mm}</span><span class="eqno">({num})</span></pre>'))
    return token
body_md = re.sub(r'\$\$\s*(.*?)\s*\$\$', block_math, body_md, flags=re.S)

inline_math=[]
def in_math(m):
    tex=m.group(1).strip()
    mm=latex_to_mathml(tex)
    token=f'PPOINLINEMATH{len(inline_math):04d}TOKEN'
    inline_math.append((token, mm))
    return token
body_md = re.sub(r'(?<!\$)\$(?!\$)([^$\n]+?)(?<!\$)\$(?!\$)', in_math, body_md)

body_html = markdown.markdown(body_md, extensions=['tables','footnotes','sane_lists','fenced_code'])
for token,val in math_blocks + inline_math:
    body_html = body_html.replace(token,val)
body_html = body_html.replace('<p>@@REFERENCES@@</p>', '\n'.join(refs_html))

# Section classes and canonical table identities.
body_html = re.sub(r'<h2>(.*?)</h2>', r'<h2 class="section">\1</h2>', body_html)
table_i=0
def table_tag(m):
    global table_i
    table_i += 1
    cls='wide long' if table_i==6 else ('wide' if table_i in (2,) else '')
    return f'<table id="table-{table_i}" data-table="{table_i}" class="{cls}">'
body_html = re.sub(r'<table>', table_tag, body_html)
assert table_i == 6, table_i
assert [int(x) for x in re.findall(r'data-equation="(\d+)"', body_html)] == list(range(1,13))
assert [int(x) for x in re.findall(r'data-figure="(\d+)"', body_html)] == list(range(1,7))
assert [int(x) for x in re.findall(r'data-table="(\d+)"', body_html)] == list(range(1,7))
assert not re.search(r'\[(?:Bel|Bro|Dua|Hee|KL|KB|Mni|Sch|SL|TET|Wan|Wil)[^]]*\]', body_html)

css = r'''
@page { size:A4; margin:13mm 14mm 14mm; }
html { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
* { box-sizing:border-box; }
body { margin:0; color:#151515; font-family:"Noto Sans CJK KR","Noto Sans KR",sans-serif; font-size:8.6pt; line-height:1.48; }
a { color:#1f5c99; text-decoration:none; }
.cover { position:relative; height:255mm; padding-left:14mm; page-break-after:always; }
.cover .bar { position:absolute; left:0; top:0; bottom:0; width:6px; background:#111; }
.cover .spacer { height:72mm; }
.cover h1 { font-size:28pt; line-height:1.12; margin:0 0 10px; padding-bottom:10px; border-bottom:3px solid #111; max-width:150mm; }
.cover .subtitle { font-size:15pt; font-weight:750; margin:12px 0 24px; }
.cover .meta { font-size:10pt; line-height:1.9; }
.cover .note { margin-top:20px; color:#666; max-width:150mm; }
.body { column-count:2; column-gap:7mm; column-fill:auto; text-align:justify; }
.body p { margin:0 0 6px; }
h1.doc-title { column-span:all; font-size:17pt; line-height:1.2; margin:0 0 7px; padding-bottom:7px; border-bottom:2px solid #111; }
h2.section { column-span:all; font-size:14pt; margin:12px 0 7px; padding:5px 0; border-top:1px solid #aaa; border-bottom:1px solid #aaa; break-after:avoid; }
h3 { font-size:10.5pt; margin:9px 0 4px; break-after:avoid; }
ul.biblist, ul.memo { margin:0 0 8px; padding-left:17px; }
.frontmatter { column-span:all; display:grid; grid-template-columns:1fr 1fr; gap:8mm; margin-bottom:10px; padding-bottom:8px; border-bottom:1px solid #bbb; }
.frontmatter h3 { margin-top:0; }
pre.equation { position:relative; display:flex; align-items:center; justify-content:center; column-span:all; white-space:normal; overflow:visible; background:#f7f8fa; border:1px solid #d8dde4; border-radius:4px; padding:8px 34px 8px 10px; margin:7px 0; break-inside:avoid; font-family:serif; }
pre.equation .math-wrap { max-width:100%; overflow:visible; }
pre.equation math { font-size:11pt; max-width:100%; }
.eqno { position:absolute; right:9px; top:50%; transform:translateY(-50%); font-family:serif; font-size:9pt; }
pre:not(.equation) { column-span:all; white-space:pre-wrap; background:#f4f4f4; border:1px solid #ddd; padding:7px 9px; font-size:8pt; line-height:1.35; break-inside:avoid; }
figure { margin:8px 0; text-align:center; break-inside:avoid; }
figure.fig-wide { column-span:all; }
figure img { display:block; max-width:100%; max-height:225mm; width:auto; height:auto; margin:auto; object-fit:contain; }
#fig-1 img { max-height:82mm; } #fig-2 img { max-height:85mm; } #fig-3 img { max-height:108mm; } #fig-4 img { max-height:82mm; } #fig-5 img { max-height:56mm; } #fig-6 img { max-height:220mm; }
figcaption { font-size:8pt; line-height:1.35; color:#444; margin-top:4px; text-align:justify; }
.table-caption { font-size:8pt; line-height:1.35; margin:5px 0 8px; break-after:avoid; }
table { width:100%; border-collapse:collapse; font-size:7.6pt; margin:5px 0; break-inside:avoid; }
table.wide, .table-caption:has(+ table.wide) { column-span:all; }
table.long { break-inside:auto; font-size:7.2pt; }
table.long tr { break-inside:avoid; }
th,td { border:.6pt solid #333; padding:2.5px 4px; vertical-align:middle; overflow-wrap:anywhere; }
th { background:#e8ebef; font-weight:700; } td:not(:first-child), th:not(:first-child) { text-align:right; }
.citation { white-space:nowrap; }
ol.refs { font-size:7.8pt; line-height:1.35; padding-left:18px; }
ol.refs li { margin-bottom:4px; break-inside:avoid; }
ol.refs p { display:inline; }
.footnote { font-size:7.5pt; }
'''

front = '''
<section class="cover"><div class="bar"></div><div class="spacer"></div>
<h1>Proximal Policy Optimization Algorithms</h1>
<div class="subtitle">한국어 전문 번역</div>
<div class="meta"><div><b>저자</b>: John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, Oleg Klimov — OpenAI</div>
<div><b>발표</b>: arXiv:1707.06347v2 [cs.LG], 2017-08-28</div>
<div><b>원문</b>: https://arxiv.org/abs/1707.06347v2</div>
<div><b>번역 생성일</b>: 2026-09-05</div></div>
<div class="note">원문의 섹션·수식·알고리즘·그림·표·부록을 보존해 2단 학술 레이아웃으로 재구성한 한국어 완역본이다.</div></section>
<div class="body"><h1 class="doc-title">Proximal Policy Optimization Algorithms — 한국어 전체 번역</h1>
<div class="frontmatter"><div><h3>서지 정보</h3><ul class="biblist">
<li><b>원문 버전</b>: arXiv:1707.06347v2</li><li><b>저자</b>: John Schulman et al. (OpenAI)</li>
<li><b>원문</b>: <a href="https://arxiv.org/abs/1707.06347v2">abstract</a> · <a href="https://arxiv.org/pdf/1707.06347v2">PDF</a></li>
<li><b>범위</b>: 초록, 본문 1–8절, 참고문헌, 부록 A–B</li></ul></div>
<div><h3>번역 메모</h3><ul class="memo"><li>policy, action, advantage, surrogate objective, clipping, rollout 등 핵심 RL 용어는 영문을 유지했다.</li>
<li>수식 (1)–(12)은 원문 구조와 번호를 static MathML로 재현했다.</li><li>표의 수치·게임명·환경명·hyperparameter 표기는 원문을 보존했다.</li>
<li>그림은 원문 PDF의 개별 figure 영역만 추출했으며 영문 캡션은 한국어로 완역했다.</li></ul></div></div>
'''

doc = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>PPO 한국어 전문 번역</title><style>{css}</style></head><body>{front}{body_html}</div></body></html>'''
(W/'translation.html').write_text(doc)

# Standalone machine-checkable structural report.
report={
 'equations':[int(x) for x in re.findall(r'data-equation="(\d+)"',doc)],
 'figures':[int(x) for x in re.findall(r'data-figure="(\d+)"',doc)],
 'tables':[int(x) for x in re.findall(r'data-table="(\d+)"',doc)],
 'references':len(refs), 'inline_math':len(inline_math),
 'unresolved_dollar':doc.count('$'), 'unresolved_citation_keys':bool(re.search(r'\[(?:Bel|Bro|Dua|Hee|KL|KB|Mni|Sch|SL|TET|Wan|Wil)',doc))
}
assert report['unresolved_dollar']==0
assert not report['unresolved_citation_keys']
(W/'structure_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps(report,ensure_ascii=False,indent=2))
