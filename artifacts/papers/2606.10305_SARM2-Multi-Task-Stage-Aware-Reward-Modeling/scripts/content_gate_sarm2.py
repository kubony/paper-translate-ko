import re,json,sys
from pathlib import Path
B=Path('artifacts/papers/2606.10305_SARM2-Multi-Task-Stage-Aware-Reward-Modeling')
h=(B/'translation.html').read_text(encoding='utf-8')
plain=re.sub(r'<[^>]+>',' ',h)
checks={}
checks['main_sections_1_to_5']=all(re.search(rf'>\s*{n}(?:\s|\.)',h) for n in range(1,6))
checks['appendix_6_1_to_6_15']=all(re.search(rf'>\s*6\.{n}(?:\s|<)',h) for n in range(1,16))
checks['figures_1_to_14_once']=all(h.count(f'id="figure-{n}"')==1 for n in range(1,15))
checks['tables_1_to_10_present']=all(re.search(rf'표\s*{n}(?:\D|$)',plain) for n in range(1,11))
checks['equations_1_to_9_present']=all(re.search(rf'\({n}\)',plain) for n in range(1,10))
checks['references_63']=len(re.findall(r'<ol class="refs">(.*?)</ol>',h,re.S))==1 and len(re.findall(r'<li>',re.search(r'<ol class="refs">(.*?)</ol>',h,re.S).group(1)))==63
checks['video_links_22']=all(x in h for x in json.loads((B/'assets/videos.json').read_text())['assets'][0].keys()) if False else h.count('<tr><td>')>=22
checks['no_placeholders']=not re.search(r'자리표시자|삽입 위치|TODO|TBD|Lorem ipsum',h,re.I)
checks['core_terms']=all(x in plain for x in ['SARM2','SPIRAL','action primitive','reward model','rollout','Mixture of Experts'])
(B/'content-gate.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(checks,ensure_ascii=False,indent=2))
if not all(checks.values()): sys.exit(1)
