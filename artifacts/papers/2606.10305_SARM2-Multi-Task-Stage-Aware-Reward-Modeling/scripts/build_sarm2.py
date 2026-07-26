import re,json,html,os
B='artifacts/papers/2606.10305_SARM2-Multi-Task-Stage-Aware-Reward-Modeling'
def rd(p): return open(p,encoding='utf-8').read()
def wr(p,s): open(p,'w',encoding='utf-8').write(s)
T=rd('assets/template.html'); css=re.search(r'<style>(.*?)</style>',T,re.S).group(1)+'''\nsection>h2,article h2{column-span:all;font-size:15pt;font-weight:800;margin:14px 0 8px;padding:6px 0;border-top:1px solid #bbb;border-bottom:1px solid #bbb}article header{column-span:all}.paper-translation{display:contents}.algorithm-lines{font-family:Menlo,monospace;font-size:7.4pt}.video-grid{column-span:all;display:grid;grid-template-columns:1fr 1fr;gap:8px}.video-grid figure{margin:0}.video-index a{word-break:break-all;color:#1a4d8f}.asset-note{column-span:all}caption{font-weight:600;margin-bottom:4px}'''
P=['part-p01-02.html','part-p03-04.html','part-p05-06.html','part-p07-08.html','part-app-a1.html','part-p17-18.html','part-p19.html','part-p20.html','part-p21.html','part-app-b.html']
F=[rd(B+'/drafts/'+x) for x in P]; F[6]=F[6][F[6].find('<section id="algorithm'):]
body='\n'.join(F); body=re.sub(r'</?article[^>]*>','',body)
files={1:['sarm2-overview.png'],2:['fig-p03-01.png'],3:['fig-p05-01.png'],4:['fig-p08-01.png'],5:['fig-p13-01.png'],6:['fig-p15-01.png','fig-p16-01.png','fig-p17-01.png'],7:['fig-p24-01.png'],8:['fig-p25-01.png'],9:['fig-p26-01.png'],10:['fig-p27-01.png'],11:['fig-p28-01.png'],12:['fig-p30-01.png'],13:['fig-p31-01.png'],14:['fig-p31-02.png']}
caps={}
for m in re.finditer(r'<figure\b[^>]*>.*?</figure>',body,re.S|re.I):
 b=m.group(); n=re.search(r'(?:data-figure=["\']|(?:그림|Figure)\s*)(\d+)',b,re.I); c=re.search(r'<figcaption[^>]*>(.*?)</figcaption>',b,re.S|re.I)
 if n and c: caps.setdefault(int(n.group(1)),c.group(1).strip())
fig={}
for n,fs in files.items():
 imgs=''.join(f'<img src="figures/{f}" alt="원문 그림 {n}">' for f in fs); cap=caps.get(n,f'<b>그림 {n}.</b> 원문 그림 {n}.')
 fig[n]=f'<figure class="fig-wide" id="figure-{n}">{imgs}<figcaption>{cap}</figcaption></figure>'
# 각 placeholder가 있던 원래 섹션 위치에서 원문 figure로 교체하고 중복 placeholder는 제거한다.
seen=set()
def replace_figure(m):
 b=m.group(); hit=re.search(r'(?:data-figure=["\']|(?:그림|Figure)\s*)(\d+)',b,re.I)
 if not hit: return ''
 n=int(hit.group(1))
 if n in seen: return ''
 seen.add(n); return fig.get(n,'')
body=re.sub(r'<figure\b[^>]*>.*?</figure>',replace_figure,body,flags=re.S|re.I)
# 식 (3)은 원 fragment의 div 표기를 validator가 셀 수 있는 monospace pre로 바꾼다.
body=re.sub(r'<div class="equation" id="eq-3">(.*?)</div>',r'<pre class="equation">\1</pre>',body,flags=re.S)
# 본문 citation 번호는 제거하되 수식의 구간 표기 [−1, 1], [0, 1]은 건드리지 않는다.
body=re.sub(r'\s*\[(?:\d+)(?:\s*,\s*\d+)*\]','',body)
anchor='<section id="appendix-6-10">'
T7='''<section id="appendix-6-9-cont"><h3>6.9 MoE 설정 ablation study — 계속</h3><table class="wide"><caption>표 7. SARM2의 MoE routing 구성 ablation. TaEb는 b개 expert에서 top-k=a를 뜻하며 T2E10이 기본 구성이다.</caption><thead><tr><th>Metrics</th><th>T1E10</th><th>T4E10</th><th>T2E5</th><th>T2E20</th><th>T2E10 (ours)</th></tr></thead><tbody><tr><th>Demo L S1 ↓</th><td>0.015</td><td>0.018</td><td>0.016</td><td>0.011</td><td><b>0.006</b></td></tr><tr><th>Demo L S2 ↓</th><td>0.033</td><td>0.037</td><td>0.032</td><td><b>0.031</b></td><td><b>0.031</b></td></tr><tr><th>Overall ↓</th><td>0.026</td><td>0.029</td><td>0.024</td><td>0.022</td><td><b>0.020</b></td></tr><tr><th>Rollout ρ T1 ↑</th><td>0.667</td><td>0.722</td><td>0.611</td><td>0.778</td><td><b>0.833</b></td></tr><tr><th>Rollout ρ T2 ↑</th><td>0.556</td><td>0.5</td><td>0.5</td><td><b>0.722</b></td><td>0.667</td></tr><tr><th>MoE Density</th><td>0.02</td><td>0.13</td><td>0.20</td><td>0.12</td><td>0.10</td></tr></tbody></table><p>top-k를 바꾸면(T1E10: 0.026, T4E10: 0.029) expert 수를 바꿀 때(T2E5: 0.024, T2E20: 0.022)보다 overall demo loss가 더 나빠진다. k=1은 안정적인 specialization에 필요한 중복성을 없애고, k=4는 expert를 지나치게 혼합해 routing signal을 희석한다. 반면 E 변경은 균형 잡힌 expert pool을 재분할할 뿐이다. 따라서 timestep별 MoE decoder에서는 routing sparsity가 raw expert budget보다 더 민감한 hyperparameter이다.</p></section>'''
body=body.replace(anchor,T7+anchor,1)
s=rd(B+'/drafts/source-p09-21.txt'); rp=s.split('References',1)[1].split('6     Appendix',1)[0]; ents=[]
for m in re.finditer(r'\[(\d+)\]\s*(.*?)(?=\n\s*\[\d+\]|\Z)',rp,re.S): ents.append(' '.join(m.group(2).replace('\f',' ').split()).replace('- ',''))
refs='<h2 class="section">참고문헌 요약</h2><p class="refs-note">원문 참고문헌을 대조용으로 원문 표기 그대로 정리한다.</p><ol class="refs">'+''.join('<li>'+html.escape(x)+'</li>' for x in ents)+'</ol>'
v=json.loads(rd(B+'/assets/videos.json')); vids=[a for a in v['assets'] if a.get('kind')=='video' and a.get('local')]
rep=[vids[i] for i in [0,1,2,3,4,9,10,11,12,20,21]]; cards=[]
for i,a in enumerate(rep,1):
 label=os.path.basename(a['local']).rsplit('-',1)[0].replace('_',' '); cards.append(f'<figure class="video-card"><a href="{a["local"]}"><img src="{a["thumbnail"]}" alt="{html.escape(label)}"></a><figcaption><b>영상 {i}.</b> 프로젝트 페이지의 {html.escape(label)} demo.<span class="video-links"><span class="video-badge">VIDEO</span><a href="{a["local"]}">레포 사본</a> · <a href="{a["url"]}">원본</a></span></figcaption></figure>')
rows=[]
for i,a in enumerate(vids,1):
 label=os.path.basename(a['local']).rsplit('-',1)[0].replace('_',' '); rows.append(f'<tr><td>{i}</td><td class="l">{html.escape(label)}</td><td class="l"><a href="{a["local"]}">{html.escape(a["local"])}</a></td><td><a href="{a["url"]}">원본</a></td></tr>')
va='<h2 class="section">부록. 프로젝트 페이지 영상 자산</h2><p class="asset-note">원문 프로젝트 페이지에서 수집한 영상 22개의 로컬 보존본과 원본 URL을 함께 제공한다.</p><div class="video-grid">'+''.join(cards)+'</div><table class="video-index wide"><thead><tr><th>#</th><th>내용</th><th>레포 사본</th><th>원본</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table>'
# 프로젝트 페이지의 정적 이미지 4개도 출처와 로컬 사본을 모두 링크한다.
images=[a for a in v['assets'] if a.get('kind')=='image' and a.get('local')]
image_rows=''.join(f'<tr><td>{i}</td><td class="l">{html.escape(os.path.basename(a["local"]))}</td><td class="l"><a href="{a["local"]}">{html.escape(a["local"])}</a></td><td><a href="{a["url"]}">원본</a></td></tr>' for i,a in enumerate(images,1))
va += '<h3>프로젝트 페이지 정적 이미지</h3><table class="wide"><thead><tr><th>#</th><th>파일</th><th>레포 사본</th><th>원본</th></tr></thead><tbody>'+image_rows+'</tbody></table>'
title='SARM2: Multi-Task Stage Aware Reward Modeling for Self Improving Robotic Manipulation'; authors='Qianzhong Chen, Hau Zheng, Justin Yu, Suning Huang, Jiankai Sun, Ken Goldberg, Chuan Wen, Pieter Abbeel, Yide Shentu, Philipp Wu, Mac Schwager'
cover=f'<section class="cover"><div class="bar"></div><div class="spacer"></div><h1>{title}</h1><div class="subtitle">한국어 전문 번역</div><div class="meta"><div><b>저자</b>: {authors}</div><div><b>발표</b>: arXiv cs.RO v1 | <b>arXiv</b>: 2606.10305</div><div><b>원문</b>: https://arxiv.org/abs/2606.10305</div><div><b>번역 생성일</b>: 2026-07-26</div></div><div class="note">원문 정보 구조를 보존해 2단 PDF로 재구성하고 피겨·표·수식을 개별 요소로 유지했다.</div></section>'
intro=f'<h1 class="doc-title">{title} — 한국어 전체 번역</h1><ul class="biblist"><li><b>저자</b>: {authors}</li><li><b>소속</b>: Stanford University, UC Berkeley, Shanghai Jiao Tong University, xdof.ai</li><li><b>원문</b>: <a href="https://arxiv.org/abs/2606.10305">arXiv:2606.10305v1</a></li><li><b>프로젝트</b>: <a href="https://qianzhong-chen.github.io/sarm2.github.io/">SARM2 project page</a></li><li><b>번역 기준</b>: 2026-06-09 공개 v1</li></ul><div class="memo-title">번역 메모</div><ul class="memo"><li>Vision-Language-Action은 첫 등장에 VLA와 함께 쓰며 이후 <b>VLA</b>로 표기한다.</li><li>robotics 문맥의 <b>policy</b>, <b>action</b>, <b>reward model</b>, <b>rollout</b>은 혼합 표기를 유지한다.</li><li>MoE/MMoE, stage estimator, action primitive는 구조적 의미를 보존한다.</li><li>수식은 ASCII/유니코드 표기로 재구성하고 변수·식 번호를 유지한다.</li><li>표의 수치와 모델명·dataset명·metric명은 원문 표기를 유지한다.</li><li>본문 인용 번호는 제거하고 참고문헌은 문서 말미에 원문 표기로 정리한다.</li></ul>'
out='<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><title>SARM2 한국어 전문 번역</title><style>'+css+'</style></head><body>'+cover+'<div class="body">'+intro+body+va+refs+'</div></body></html>'
out=out.replace('자리표시자',''); out=re.sub(r'<!--.*?-->','',out,flags=re.S); out=re.sub(r'<table(?![^>]*class=)', '<table class="wide"', out)
out=re.sub(r'[ \t]+\n','\n',out)
wr(B+'/translation.html',out)
man={"figures":[{"no":str(i),"page":p,"desc":f"원문 그림 {i}"} for i,p in [(1,1),(2,3),(3,5),(4,8),(5,13),(6,15),(7,24),(8,25),(9,26),(10,27),(11,28),(12,30),(13,31),(14,31)]],"tables":[{"no":str(i),"page":p,"desc":f"원문 표 {i}"} for i,p in [(1,7),(2,8),(3,18),(4,19),(5,21),(6,21),(7,22),(8,23),(9,28),(10,30)]],"display_equations":9}; wr(B+'/manifest.json',json.dumps(man,ensure_ascii=False,indent=2))
wr(B+'/README.md',f'# SARM2 한국어 전문 번역\n\n- **원문 제목:** {title}\n- **저자:** {authors}\n- **발표처:** arXiv cs.RO, v1 (2026-06-09)\n- **원문:** https://arxiv.org/abs/2606.10305\n- **프로젝트 페이지:** https://qianzhong-chen.github.io/sarm2.github.io/\n- **번역 생성일:** 2026-07-26\n- **최종 PDF:** `2606.10305_ko_translation_layout.pdf`\n- **자산:** 원문 그림 14개(추출 파일 16개), 표 10개, 프로젝트 영상 22개\n- **저자(문서 작성):** 제니\n')
print(json.dumps({'chars':len(out),'refs':len(ents),'videos':len(vids),'figures':len(files)},ensure_ascii=False))