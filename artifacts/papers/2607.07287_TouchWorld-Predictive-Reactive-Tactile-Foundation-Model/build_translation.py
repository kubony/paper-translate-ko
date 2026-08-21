#!/usr/bin/env python3
import html, json, re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
from latex2mathml.converter import convert as latex_to_mathml
from pylatexenc.latex2text import LatexNodes2Text
import bibtexparser

ROOT=Path(__file__).resolve().parent
FRAGS=['01a_abstract_intro.html','01b_method.html','02_training_experiments.html','03a_discussion_conclusion.html','03b_appendix_related.html','03c_appendix_implementation.html']
parts=[]
for name in FRAGS:
    parts.append((ROOT/'fragments'/name).read_text())
body='\n'.join(parts)
# Independently audited corrections and canonical numbering.
body=body.replace('각 task의 human-perturbation variant인 Water Flower, Tabletop Clearing, Cup Insertion, Power Plug Insertion, Pot Wiping, Tissue Pulling에서 평가한다.', 'Water Flower, Tabletop Clearing, Cup Insertion, Power Plug Insertion, Pot Wiping, Tissue Pulling의 여섯 real-robot task와 각 task의 human-perturbation variant에서 평가한다.')
body=body.replace('Wuji dexterous hand와 JQ-Industries tactile glove', 'Wuji dexterous hands와 JQ-Industries tactile glove')
body=body.replace('Wuji dexterous hand를 장착한', 'Wuji dexterous hands를 장착한')
body=body.replace('Meta Quest Touch Plus controller, Wuji Glove', 'Meta Quest Touch Plus controllers, Wuji Glove')
body=body.replace('Meta Quest Touch Plus controller와 Wuji Glove', 'Meta Quest Touch Plus controllers와 Wuji Glove')
body=body.replace('<h2>3 방법</h2>','<h2>2 방법</h2>').replace('<h3>3.1 ','<h3>2.1 ').replace('<h3>3.2 ','<h3>2.2 ').replace('<h3>3.3 ','<h3>2.3 ')
body=body.replace('<h2>4 학습</h2>','<h2>3 학습</h2>').replace('<h3>4.1 ','<h3>3.1 ').replace('<h3>4.2 ','<h3>3.2 ').replace('<h3>4.3 ','<h3>3.3 ').replace('<h3>4.4 ','<h3>3.4 ')
body=body.replace('<h2>5 실험</h2>','<h2>4 실험</h2>')
for a,b in [('5.1','4.1'),('5.2','4.2'),('5.3','4.3'),('5.4','4.4'),('5.5','4.5'),('5.6','4.6'),('5.7','4.7')]: body=body.replace(f'<h3>{a} ',f'<h3>{b} ')
body=body.replace('<h2>6 논의 및 한계</h2>','<h2>5 논의 및 한계</h2>').replace('<h2>7 결론</h2>','<h2>6 결론</h2>')

soup=BeautifulSoup(body,'html.parser')
# canonical source labels and ids
label_ids={'sec:method':'sec-method','sec:high_level_planning':'sec-high-level-planning','sec:goal_conditioned_policy':'sec-goal-conditioned-policy','sec:tactile_refinement_policy':'sec-tactile-refinement-policy','sec:training':'sec-training','sec:experiments':'sec-experiments','fig:teaser':'fig-1','fig:architecture':'fig-2','fig:hardware':'fig-3','fig:task_suite':'fig-4','fig:ablations':'fig-5','fig:inference_demo':'fig-6','tab:main_results':'table-1','tab:twm_prediction':'table-2','tab:planner_metrics':'table-3'}
# sections/headings
for sec,label in [(soup.select_one('section[data-section="method"]'),'sec:method'),(soup.select_one('section[data-section="training"]'),'sec:training'),(soup.select_one('section[data-section="experiments"]'),'sec:experiments')]:
    sec['data-source-label']=label; sec['id']=label_ids[label]
for text,label in [('High-Level Planning Layer','sec:high_level_planning'),('Visuo-Tactile Goal-Conditioned Policy','sec:goal_conditioned_policy'),('Tactile-Conditioned Refinement Policy','sec:tactile_refinement_policy')]:
    h=next(h for h in soup.find_all('h3') if text in h.get_text())
    h['data-source-label']=label; h['id']=label_ids[label]
# figures and tables
for fig in soup.find_all('figure'):
    label=fig.get('data-source-label') or fig.get('data-label')
    fig.attrs.pop('data-label',None); fig['data-source-label']=label; fig['id']=label_ids[label]; fig['class']=['fig-wide']
    n=fig['data-figure']
    ph=fig.find(class_='figure-placeholder')
    img=soup.new_tag('img',src=f'figures/figure-{n}.png',alt=f'TouchWorld 그림 {n}')
    ph.replace_with(img)
for table in soup.find_all('table'):
    label=table.get('data-source-label') or table.get('data-label')
    table.attrs.pop('data-label',None); table['data-source-label']=label; table['id']=label_ids[label]
    table['class']=['wide'] if table['data-table']=='1' else ['compact']
# cross refs
xref_names={'sec:goal_conditioned_policy':'2.2절','fig:hardware':'그림 3','fig:task_suite':'그림 4','fig:ablations':'그림 5','fig:inference_demo':'그림 6','tab:main_results':'표 1','tab:twm_prediction':'표 2','tab:planner_metrics':'표 3'}
for node in list(soup.find_all(string=re.compile(r'\[\[REF:'))):
    chunks=re.split(r'(\[\[REF:[^\]]+\]\])',str(node)); out=[]
    for c in chunks:
        m=re.fullmatch(r'\[\[REF:([^\]]+)\]\]',c)
        if m:
            lab=m.group(1); a=soup.new_tag('a',href='#'+label_ids[lab]); a['class']='xref'; a['data-source-ref']=lab; a.string=xref_names[lab]; out.append(a)
        elif c: out.append(NavigableString(c))
    for x in reversed(out): node.insert_after(x)
    node.extract()
# bibliography order and metadata
bbl=(ROOT/'source/paper.bbl').read_text()
keys=re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}',bbl,re.S)
with open(ROOT/'source/references.bib') as f: bib=bibtexparser.load(f)
entries={e['ID']:e for e in bib.entries}
citation_map={k:i+1 for i,k in enumerate(keys)}
(ROOT/'citation_map.json').write_text(json.dumps(citation_map,ensure_ascii=False,indent=2))
def citation_html(raw):
    nums=[citation_map[k.strip()] for k in raw.split(',')]
    nums=sorted(dict.fromkeys(nums)); groups=[]; i=0
    while i<len(nums):
        j=i
        while j+1<len(nums) and nums[j+1]==nums[j]+1: j+=1
        if j-i>=2: groups.append(f'<a href="#ref-{nums[i]}">{nums[i]}–{nums[j]}</a>')
        else:
            for q in range(i,j+1): groups.append(f'<a href="#ref-{nums[q]}">{nums[q]}</a>')
        i=j+1
    return '<span class="citation">['+', '.join(groups)+']</span>'
# citations in text/attrs are text nodes
for node in list(soup.find_all(string=re.compile(r'\\cite\{'))):
    text=str(node).replace('~\\cite','\\cite')
    chunks=re.split(r'(\\cite\{[^}]+\})',text); out=[]
    for c in chunks:
        m=re.fullmatch(r'\\cite\{([^}]+)\}',c)
        if m: out.append(BeautifulSoup(citation_html(m.group(1)),'html.parser'))
        elif c: out.append(NavigableString(c.replace('~',' ')))
    for x in reversed(out): node.insert_after(x)
    node.extract()
# equations: exact active source latex
EQS=[r'\ell_t^{\mathrm{sub}} = \pi_{\mathrm{subtask}}(\ell, \mathcal{I}_t, m_t)',r'g_t = \pi_{\mathrm{world}}(\ell, \ell_t^{\mathrm{sub}}, \mathcal{I}_t, \mathcal{X}_t)',r'\left(\hat{\mathbf{A}}_{t:t+H-1}, \mathbf{c}_t\right) = \pi_{\mathrm{goal}}(\ell, \ell_t^{\mathrm{sub}}, g_t, \mathcal{I}_t, \mathbf{s}_t, \mathcal{X}_t)',r'\tilde{\mathbf{A}}_{\tau:\tau+W-1} = \pi_{\mathrm{tactile}}(\hat{\mathbf{A}}_{\tau:\tau+W-1}, \mathbf{s}_{\tau-k:\tau}, \mathcal{X}_{\tau-k:\tau}, \mathbf{c}_t)',r'o_t^{\mathrm{sub}} = \{\ell, \ell_t^{\mathrm{sub}}, r_t\}',r'\ell_{\mathrm{policy}} = \texttt{Task: } \ell \oplus \texttt{ Current subtask: } \ell_t^{\mathrm{sub}}',r'\Delta \mathbf{A}_{\tau:\tau+W-1} = f_{\phi}(\hat{\mathbf{A}}_{\tau:\tau+W-1}, \mathbf{s}_{\tau-k:\tau}, \mathcal{X}_{\tau-k:\tau}, \mathbf{c}_t)',r'\tilde{\mathbf{A}}_{\tau:\tau+W-1} = \hat{\mathbf{A}}_{\tau:\tau+W-1} + \Delta \mathbf{A}_{\tau:\tau+W-1}',r'\mathcal{L}_{\mathrm{fb}} = \left\| f_{\phi}(\hat{\mathbf{A}}_{\tau:\tau+W-1}, \mathbf{s}_{\tau-k:\tau}, \mathcal{X}_{\tau-k:\tau}, \mathbf{c}_t) - (\mathbf{A}^{*}_{\tau:\tau+W-1} - \hat{\mathbf{A}}_{\tau:\tau+W-1}) \right\|_2^2']
for n,tex in enumerate(EQS,1):
    tag=soup.select_one(f'[data-equation="{n}"]')
    tag.name='pre'; tag.clear(); tag['class']=['equation']; tag['data-source-latex']=tex
    math=BeautifulSoup(latex_to_mathml(tex),'html.parser').find('math'); tag.append(math)
    span=soup.new_tag('span'); span['class']='equation-number'; span.string=f'({n})'; tag.append(span)
# inline math
skip_names={'math','script','style'}
for node in list(soup.find_all(string=re.compile(r'\$[^$]+\$'))):
    if node.parent.name in skip_names: continue
    chunks=re.split(r'(\$[^$]+\$)',str(node)); out=[]
    for c in chunks:
        if c.startswith('$') and c.endswith('$'):
            tex=c[1:-1]
            try: out.append(BeautifulSoup(latex_to_mathml(tex),'html.parser').find('math'))
            except Exception: out.append(NavigableString(c))
        elif c: out.append(NavigableString(c))
    for x in reversed(out): node.insert_after(x)
    node.extract()
# visible latex escapes
for node in soup.find_all(string=True):
    if node.parent.name not in {'math','script','style'}:
        node.replace_with(str(node).replace('\\%','%').replace('\\times','×'))
# videos appendix
videos=json.loads((ROOT/'assets/videos.json').read_text())['assets']
vs=soup.new_tag('section'); vs['class']='video-assets'; h=soup.new_tag('h2'); h.string='프로젝트 페이지 영상 자산'; vs.append(h)
intro=soup.new_tag('p'); intro.string='논문 프로젝트 페이지에 공개된 TouchWorld 시연과 Tactile World Model 예측 영상을 원문 자산과 함께 보존한다.'; vs.append(intro)
titles=['Spray Water 전체 시연','Spray Water 실행 episode','Tactile World Model ground truth','Tactile World Model prediction']
for idx,(v,title) in enumerate(zip(videos,titles),1):
    f=soup.new_tag('figure'); f['class']='video-card'
    a=soup.new_tag('a',href=v['local']); img=soup.new_tag('img',src=v['thumbnail'],alt=title); a.append(img); f.append(a)
    cap=soup.new_tag('figcaption'); cap.append(BeautifulSoup(f'<b>영상 {idx}.</b> {title} — {v["duration_s"]:.2f}초. ▶ <a href="{v["local"]}">레포 사본</a> · <a href="{v["url"]}">원본</a>','html.parser')); f.append(cap); vs.append(f)
soup.append(vs)
# References
refs=soup.new_tag('section'); refs['class']='references'; h=soup.new_tag('h2'); h.string='참고문헌'; refs.append(h); ol=soup.new_tag('ol')
cleaner=LatexNodes2Text()
for n,k in enumerate(keys,1):
    e=entries.get(k,{})
    author=cleaner.latex_to_text(e.get('author','Unknown')).split(' and ')[0].replace('{','').replace('}','')
    year=cleaner.latex_to_text(e.get('year','n.d.')).replace('{','').replace('}','')
    title=cleaner.latex_to_text(e.get('title',k)).replace('{','').replace('}','')
    li=soup.new_tag('li',id=f'ref-{n}'); li['data-cite-key']=k; li.string=f'{author} et al. ({year}). {title}.'; ol.append(li)
refs.append(ol); soup.append(refs)

CSS='''
@page { size:A4; margin:14mm 15mm 15mm; }
*{box-sizing:border-box} body{margin:0;color:#18222d;font-family:"Noto Sans KR","Noto Sans CJK KR",Arial,sans-serif;font-size:9.25pt;line-height:1.55;word-break:keep-all;overflow-wrap:anywhere}.cover{height:268mm;page-break-after:always;display:flex;flex-direction:column;justify-content:space-between;border-left:10px solid #215d78;padding:18mm 15mm 14mm}.cover h1{font-size:29pt;line-height:1.15;margin:0 0 8mm;border-bottom:3px solid #215d78;padding-bottom:8mm}.cover .ko{font-size:17pt;font-weight:700;color:#215d78}.cover .meta{font-size:10.5pt;line-height:1.75}.front{column-span:all;border:1px solid #b9cbd5;background:#f4f8fa;padding:5mm;margin-bottom:7mm}.front-grid{display:grid;grid-template-columns:1fr 1fr;gap:8mm}.paper{column-count:2;column-gap:8mm;column-rule:none}.paper section{margin:0 0 5mm}.paper h2{column-span:all;font-size:15pt;margin:7mm 0 4mm;border-top:2px solid #215d78;border-bottom:1px solid #9eb8c5;padding:2.5mm 0;color:#173f53;break-after:avoid}.paper h3{font-size:10.5pt;color:#215d78;margin:4mm 0 1.5mm;break-after:avoid}.paper p{margin:0 0 2.5mm;text-align:justify}.paper ul{margin:1mm 0 3mm;padding-left:5mm}.paper li{margin-bottom:1.2mm}figure{margin:3mm 0;break-inside:avoid}figure img{display:block;width:100%;height:auto}.fig-wide,.video-assets{column-span:all}.paper figure figcaption,.paper table caption{font-size:8pt;line-height:1.4;text-align:left;margin-top:1.2mm}.equation{position:relative;display:flex;align-items:center;justify-content:center;min-height:12mm;margin:3mm 0;padding:2mm 9mm 2mm 2mm;break-inside:avoid;background:#f8fafb;border-left:2px solid #8fb0c0;overflow:hidden;white-space:normal;font-family:inherit}.equation math{font-size:10pt;max-width:100%}.equation-number{position:absolute;right:2mm;font-weight:600}table{border-collapse:collapse;width:100%;font-size:7.2pt;margin:3mm 0;break-inside:avoid}table.wide{column-span:all;font-size:7.5pt}th,td{border:1px solid #aebcc5;padding:1.3mm 1mm;text-align:center}th{background:#eaf1f4}.citation{white-space:nowrap;font-size:8pt}.xref{white-space:nowrap;color:#12648b;text-decoration:none}.video-assets{display:grid;grid-template-columns:1fr 1fr;gap:4mm 6mm}.video-assets h2,.video-assets>p{grid-column:1/-1}.video-card{border:1px solid #bacad3;padding:2mm;background:#f7fafb}.video-card img{aspect-ratio:16/9;object-fit:cover}.references ol{padding-left:5mm;font-size:7.2pt}.references li{break-inside:avoid;margin-bottom:1.2mm}.appendix-implementation-details{} a{color:#135f82}.footer-note{font-size:7.5pt;color:#52626c}
'''
cover='''<section class="cover"><div><div class="ko">한국어 전문 번역</div><h1>TouchWorld: A Predictive and Reactive Tactile Foundation Model for Dexterous Manipulation</h1><p style="font-size:15pt">촉각 기반 dexterous manipulation을 위한 예측·반응형 tactile foundation model</p></div><div class="meta"><b>저자:</b> Jianyi Zhou, Feiyang Hong, Yunhao Li, Yicheng Zhao, Yongjue Cen, Zirui Liu, Jiakang Huang, Zirui Chen, Ruiyang Zhang, Weizhuo Zhu, Xuhua Song, Shuo Yang<br><b>소속:</b> Harbin Institute of Technology, Shenzhen · PHANES AI<br><b>arXiv:</b> 2607.07287v2 · cs.RO<br><b>원문:</b> https://arxiv.org/abs/2607.07287v2<br><b>프로젝트:</b> https://phanes-lab.github.io/TouchWorld-website/<br><b>번역 생성일:</b> 2026-08-21</div><div class="footer-note">논문과 유사한 2단 학술 PDF 레이아웃으로 구성했으며, 원문 피겨·표·수식·수치를 보존했다. 번역은 원문 v2를 기준으로 한다.</div></section>'''
front='''<section class="front"><div class="front-grid"><div><b>서지 및 원문</b><ul><li>원제: TouchWorld: A Predictive and Reactive Tactile Foundation Model for Dexterous Manipulation</li><li>버전: arXiv:2607.07287v2 (2026-07-09)</li><li>분야: Robotics (cs.RO)</li><li>프로젝트 페이지 영상 4건을 로컬 자산으로 보존했다.</li></ul></div><div><b>번역 메모</b><ul><li>tactile, policy, action, control, nominal/residual은 기술 문맥을 위해 혼합 표기한다.</li><li>dexterous manipulation은 첫 문맥에서 촉각 기반 정교 조작의 의미로 읽되 원어를 유지한다.</li><li>foundation model은 파운데이션 모델, VLA는 VLA/비전-언어-액션으로 표기한다.</li><li>embodiment는 robot 몸체 문맥을 유지하며 ‘실체’로 옮기지 않는다.</li><li>모델명·데이터셋명·metric·수치·하이퍼파라미터는 원문 표기를 보존한다.</li></ul></div></div></section>'''
DOC=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>TouchWorld 한국어 전문 번역</title><style>{CSS}</style></head><body>{cover}<main class="paper">{front}{str(soup)}</main></body></html>'''
(ROOT/'translation.html').write_text(DOC)
print('built',ROOT/'translation.html','citations',len(keys),'figures',len(soup.find_all('figure')),'tables',len(soup.find_all('table')),'equations',len(soup.select('[data-equation]')))
