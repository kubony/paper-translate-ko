#!/usr/bin/env python3
from pathlib import Path
import json, re, html
import markdown

BASE = Path(__file__).resolve().parent
FRAGS = [
    BASE/'fragments/part1a1.md', BASE/'fragments/part1a2.md', BASE/'fragments/part1a3.md',
    BASE/'fragments/part1b.md', BASE/'fragments/part2.md', BASE/'fragments/part3.md'
]

FIGURES = {
'fig:arch': (2, 'model_architecture.png', True),
'fig:prompt': (3, 'prompts_v4.png', True),
'fig:robots': (4, 'pi07robots_v5.png', False),
'fig:multi_task_film_strip': (5, 'full_film_strip.png', True),
'fig:distillation_results': (6, 'distillation_results.png', True),
'fig:distillation_ablations': (7, 'distillation_ablations.png', True),
'fig:memory': (8, 'history.png', False),
'fig:instruction_following': (9, 'instruction_following.png', True),
'fig:instruction_generalization': (10, 'instruction_generalization.png', False),
'fig:compositional_generalization': (11, 'compositional_generalization.png', False),
'fig:cross_embodiment': (12, 'cross_embodiment.png', True),
'fig:human_vs_policy': (13, 'human_vs_policy.png', False),
'fig:air_fryer_coaching': (14, 'airfryer_film_strip.png', True),
'fig:long_horizon_task_generalization': (15, 'long_horizon_task_generalization.png', False),
'fig:coaching': (16, 'coaching.png', False),
'fig:task_generalization': (17, 'task_generalization.png', False),
'fig:generalization_and_conditioning': (18, 'generalization_and_conditioning_full.png', True),
'app:attention_masks': (19, 'attention_masks.png', False),
'fig:xemb_joint_vs_ee': (20, 'xemb_joint_vs_ee.png', True),
'fig:operator_stats': (21, 'operator_experience_hours.png', False),
'fig:human_vs_policy_quantitative': (22, 'human_vs_pi07.png', False),
}

VIDEO_TITLES = [
'π0.7 소개 영상', '애호박 썰기', 'espresso 만들기', '셔츠 접기', '쓰레기 내다 버리기',
'pinwheel 조립', '무지개 당근 껍질 벗기기', '나사 체결', '다양한 의류 접기',
'air fryer zero-shot 시도', 'air fryer coarse coaching', 'air fryer detailed coaching',
'air fryer high-level policy 실행', 'DROID air fryer episode', 'Galaxea air fryer 학습 episode',
'Clippi air fryer 학습 episode', '상호작용식 책상 정리 demonstration', 'ARX 셔츠 접기 teleoperation',
'UR5e 셔츠 접기와 생성 subgoal overlay', '오이 껍질 벗기기', '땅콩버터 샌드위치 만들기',
'Windex로 유리문 청소', '애호박 껍질 벗기기', '청바지 접기', '옷 바로 뒤집기', '문을 열고 통과해 주행하기'
]

def inline_md(s: str) -> str:
    s = markdown.markdown(s, extensions=[]).strip()
    if s.startswith('<p>') and s.endswith('</p>'):
        s = s[3:-4]
    return s

def figure_html(label: str, caption: str) -> str:
    no, filename, wide = FIGURES[label]
    cls = ' class="fig-wide"' if wide else ''
    return (f'<figure{cls} data-figure="{no}">\n'
            f'<img src="figures_source/{filename}" alt="그림 {no}">\n'
            f'<figcaption><b>그림 {no}.</b> {inline_md(caption)}</figcaption>\n</figure>')

def clean_fragment(text: str) -> str:
    out=[]
    for line in text.splitlines():
        if re.match(r'^\[P[123A-Z0-9-]+\s*[|\]]', line):
            continue
        if re.match(r'^\*\*P2-\d+ \(source lines?', line):
            continue
        if re.match(r'^\*\*\[P3-\d+ \| source lines?', line):
            # Preserve any semantic label after the metadata closing marker.
            tail = re.sub(r'^\*\*\[P3-\d+ \| source lines?[^\]]+\]\*\*\s*', '', line)
            if tail: out.append(tail)
            continue
        if line.startswith('# π0.7: 조종 가능한 범용 로봇 파운데이션 모델 — 제3부'):
            continue
        if line.startswith('> 번역 범위:'):
            continue
        out.append(line)
    text='\n'.join(out)
    # Contribution/task-rubric paragraphs carry their source marker inside the
    # same bold span as the semantic paragraph label. Remove only the marker.
    text=re.sub(r'\*\*\[P3-\d+ \| source lines?[^\]]+\]\s*', '**', text)
    # Canonical section numbering from main.tex active section order.
    for a,b in [('(7.1절)','(9.1절)'),('(7.2절)','(9.2절)'),('(7.3절)','(9.3절)'),('(7.4절)','(9.4절)'),('(7.5절)','(9.5절)'),('여기에는 7절의 작업','여기에는 9절의 작업'),('7.1절에서 보이듯','9.1절에서 보이듯')]:
        text=text.replace(a,b)
    # Display equations: exactly three semantic equations.
    text=text.replace('**max_θ E_{𝒟}[log π_θ(𝐚_{t:t+H} | 𝐨_{t−T:t}, 𝒞_t)].**',
                      '<pre class="equation" data-equation="1">max_θ E_{𝒟}[log π_θ(𝐚_{t:t+H} | 𝐨_{t−T:t}, 𝒞_t)]    (1)</pre>')
    text=text.replace('max_ψ E_{𝒟_g}[L_CFM(𝐠ₜ★, gψ(𝐨ₜ, ℓ̂ₜ, m))]',
                      '<pre class="equation" data-equation="2">max_ψ E_{𝒟_g}[L_CFM(𝐠ₜ★, gψ(𝐨ₜ, ℓ̂ₜ, m))]    (2)</pre>')
    text=text.replace('$\\pi_{0.6}\\texttt{-MEM}$', 'π₀.₆-MEM')
    text=re.sub(r'EQUATION 1:\s*```text\s*(.*?)\s*```',
                lambda m: '<pre class="equation" data-equation="3">'+html.escape(m.group(1).strip())+'    (3)</pre>',
                text, flags=re.S)
    # Figures 2 and 3 use literal caption prefixes in the translated fragment.
    text=re.sub(r'^\*\*그림 2\. 아키텍처 개요\.\*\*\s*(.*)$',
                lambda m: figure_html('fig:arch', '<b>아키텍처 개요.</b> '+m.group(1)), text, flags=re.M)
    text=re.sub(r'^\*\*그림 3\. Prompt 개요\.\*\*\s*(.*)$',
                lambda m: figure_html('fig:prompt', '<b>Prompt 개요.</b> '+m.group(1)), text, flags=re.M)
    # All remaining translated figure markers.
    lines=[]
    pat_plain=re.compile(r'^FIGURE ([A-Za-z0-9_:.-]+):\s*(.*)$')
    pat_bold=re.compile(r'^\*\*FIGURE ([A-Za-z0-9_:.-]+):\*\*\s*(.*)$')
    for line in text.splitlines():
        m=pat_plain.match(line) or pat_bold.match(line)
        if m and m.group(1) in FIGURES:
            lines.append(figure_html(m.group(1), m.group(2)))
        else:
            lines.append(line)
    text='\n'.join(lines)
    # Convert source-label prose references to the visible figure numbering.
    for label,(no,_,_) in FIGURES.items():
        text=text.replace('FIGURE '+label, f'그림 {no}')
        text=text.replace('Figure '+label, f'그림 {no}')
    return text

def normalize_headings(body_html: str) -> str:
    def repl(m):
        inner=m.group(2)
        plain=re.sub('<[^>]+>', '', inner).strip()
        full = (plain in {'초록','감사의 말','부록','참고문헌 요약'} or
                bool(re.match(r'^(?:[1-9]|10)\.\s(?!\d)', plain)))
        if full:
            return f'<h2 class="section">{inner}</h2>'
        return f'<h3>{inner}</h3>'
    return re.sub(r'<h([1-6])>(.*?)</h\1>', repl, body_html, flags=re.S)

def video_appendix() -> str:
    data=json.loads((BASE/'assets/videos.json').read_text())
    vids=[a for a in data['assets'] if a['kind']=='video']
    assert len(vids)==len(VIDEO_TITLES)==26
    rows=[]
    for i,(v,title) in enumerate(zip(vids,VIDEO_TITLES),1):
        rows.append(f'<tr><td>{i}</td><td class="l">{html.escape(title)}</td>'
                    f'<td class="l"><a href="{html.escape(v["local"])}">레포 사본</a></td>'
                    f'<td class="l"><a href="{html.escape(v["url"])}">원본</a></td></tr>')
    video_table = ('<h2 class="section">부록. 프로젝트 페이지 영상 자산</h2>'
            '<p>논문의 공식 프로젝트 페이지에서 수집한 원문 영상 26개를 보존했다. PDF에서는 재생되지 않으므로 아래 링크로 로컬 보존본 또는 원본을 연다.</p>'
            '<table class="video-index wide"><thead><tr><th>#</th><th class="l">내용</th><th>보존본</th><th>원본</th></tr></thead><tbody>'+
            ''.join(rows)+'</tbody></table>')
    image_table = '''<h2 class="section">부록. 프로젝트 페이지 정적 자산</h2>
<p>공식 프로젝트 페이지의 대표 이미지와 사이트 아이콘도 재현·추적 가능하도록 함께 보존했다.</p>
<table class="video-index wide"><thead><tr><th>#</th><th class="l">내용</th><th>보존본</th><th>원본</th></tr></thead><tbody>
<tr><td>1</td><td class="l">π0.7 프로젝트 대표 이미지</td><td><a href="assets/images/pi07-og-78b56a.png">레포 사본</a></td><td><a href="https://physicalintelligence.company/images/pi07/pi07-og.png">원본</a></td></tr>
<tr><td>2</td><td class="l">프로젝트 사이트 아이콘(light)</td><td><a href="assets/images/icon-4cfe64.png">레포 사본</a></td><td><a href="https://www.pi.website/icon.png">원본</a></td></tr>
<tr><td>3</td><td class="l">프로젝트 사이트 아이콘(dark)</td><td><a href="assets/images/icon-dark-63c206.png">레포 사본</a></td><td><a href="https://www.pi.website/icon-dark.png">원본</a></td></tr>
</tbody></table>'''
    return video_table + image_table

raw='\n\n'.join(clean_fragment(p.read_text()) for p in FRAGS)
body=markdown.markdown(raw, extensions=['tables','fenced_code'])
body=normalize_headings(body)
body=body.replace('<ol>', '<ol class="refs">', 1 if '참고문헌 요약' in body else 0)

teaser=figure_html('fig:teaser' if False else 'fig:arch','') if False else '''
<figure class="fig-wide" data-figure="1">
<img src="figures_source/fig1.png" alt="그림 1">
<figcaption><b>그림 1.</b> 조종 가능한 범용 로봇 파운데이션 모델 π0.7은 여러 task, environment, robot에서 dexterous task를 수행한다. π0.7은 task 설명뿐 아니라 상세 언어, 생성 subgoal image, episode metadata를 포함하는 다양한 prompt로 학습한다. 이 context는 무엇을 할지뿐 아니라 어떻게 수행할지도 제공하여, 로봇·비로봇 데이터의 광범위한 skill을 새로운 방식으로 조합해 새 task를 해결할 수 있게 한다.</figcaption>
</figure>'''

css='''
@page { size:A4; margin:15mm; }
html { -webkit-print-color-adjust:exact; print-color-adjust:exact; }
* { box-sizing:border-box; }
body { font-family:"Noto Sans KR","Apple SD Gothic Neo",sans-serif; color:#111; font-size:9.2pt; line-height:1.52; margin:0; }
a { color:#174f8a; text-decoration:none; }
.cover { position:relative; min-height:250mm; padding-left:14mm; page-break-after:always; }
.cover .bar { position:absolute; left:0; top:0; bottom:0; width:6px; background:#111; }
.cover .spacer { height:64mm; }
.cover h1 { font-size:27pt; font-weight:800; line-height:1.15; margin:0 0 6px; padding-bottom:10px; border-bottom:3px solid #111; max-width:155mm; }
.cover .subtitle { font-size:14pt; font-weight:700; margin:10px 0 20px; }
.cover .meta { font-size:10pt; line-height:1.75; }
.cover .note { margin-top:18px; font-size:9pt; color:#666; max-width:155mm; }
.body { column-count:2; column-gap:7mm; column-fill:auto; text-align:justify; }
.body p { margin:0 0 7px; }
h1.doc-title { column-span:all; font-size:17pt; font-weight:800; margin:0 0 6px; padding-bottom:8px; border-bottom:2px solid #111; line-height:1.2; }
h2.section { column-span:all; font-size:14pt; font-weight:800; margin:14px 0 8px; padding:5px 0; border-top:1px solid #bbb; border-bottom:1px solid #bbb; }
h3 { font-size:10.8pt; font-weight:800; margin:10px 0 4px; break-after:avoid; }
ul.biblist, ul.memo { margin:0 0 8px; padding-left:16px; }
ul.biblist li, ul.memo li { margin-bottom:3px; }
.memo-title { font-weight:800; font-size:12pt; margin:7px 0 4px; }
pre { font-family:"DejaVu Sans Mono",monospace; font-size:8.2pt; line-height:1.35; background:#f4f4f4; border:1px solid #ddd; border-radius:3px; padding:7px 9px; white-space:pre-wrap; word-break:break-word; break-inside:avoid; }
code { font-family:"DejaVu Sans Mono",monospace; font-size:8.5pt; background:#f0f0f0; padding:0 2px; }
figure { margin:8px 0; text-align:center; break-inside:avoid; }
figure.fig-wide { column-span:all; }
figure img { max-width:100%; height:auto; max-height:225mm; object-fit:contain; }
figcaption { font-size:8.3pt; color:#444; margin-top:4px; text-align:justify; }
figcaption b { color:#111; }
table { width:100%; border-collapse:collapse; font-size:8pt; margin:6px 0; }
table.wide { column-span:all; }
th,td { border:.6pt solid #222; padding:3px 4px; text-align:center; vertical-align:middle; overflow-wrap:anywhere; }
th { background:#e8e8e8; font-weight:700; }
td.l,th.l { text-align:left; }
table:not(.video-index) { break-inside:avoid; }
table.video-index { break-inside:auto; }
table.video-index tr { break-inside:avoid; }
ol.refs { margin:0; padding-left:18px; font-size:8.3pt; line-height:1.35; }
ol.refs li { margin-bottom:3px; }
blockquote { margin:4px 0 8px 12px; color:#444; }
'''

title='π₀.₇: a Steerable Generalist Robotic Foundation Model with Emergent Capabilities'
authors='Physical Intelligence — Bo Ai, Ali Amin, Raichelle Aniceto, Ashwin Balakrishna, Greg Balke, Kevin Black et al. (전체 저자 목록은 원문 표지 참조)'
front=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{title} — 한국어 전문 번역</title><style>{css}</style></head><body>
<section class="cover"><div class="bar"></div><div class="spacer"></div><h1>{title}</h1><div class="subtitle">한국어 전문 번역</div><div class="meta">
<div><b>저자</b>: {authors}</div><div><b>발표</b>: arXiv v2 (2026-04-24) · cs.LG / cs.RO</div><div><b>arXiv</b>: 2604.15483</div><div><b>원문</b>: <a href="https://arxiv.org/abs/2604.15483">https://arxiv.org/abs/2604.15483</a></div><div><b>프로젝트</b>: <a href="https://www.pi.website/blog/pi07">https://www.pi.website/blog/pi07</a></div><div><b>번역 생성일</b>: 2026-08-02</div><div><b>번역·편집</b>: 제니</div></div>
<div class="note">원문의 section 구조와 2단 학술 레이아웃을 보존해 완역했으며, 원문 figure 22개를 source-native asset에서 재삽입하고 algorithm을 HTML table로 재구성했다.</div></section>
<div class="body"><h1 class="doc-title">{title} — 한국어 전체 번역</h1>
<ul class="biblist"><li><b>원문 제목</b>: {title}</li><li><b>저자</b>: {authors}</li><li><b>버전</b>: arXiv v2, 2026-04-24</li><li><b>원문 PDF</b>: <a href="https://arxiv.org/pdf/2604.15483v2">https://arxiv.org/pdf/2604.15483v2</a></li><li><b>공식 프로젝트</b>: <a href="https://www.pi.website/blog/pi07">pi.website/blog/pi07</a></li><li><b>번역·편집자</b>: 제니</li></ul>
<div class="memo-title">번역 메모</div><ul class="memo"><li><b>robotic foundation model</b>은 ‘로봇 파운데이션 모델’로 표기한다.</li><li><b>VLA</b>는 첫 등장에 Vision-Language-Action(VLA, 비전-언어-액션)으로 병기하고 이후 VLA로 유지한다.</li><li><b>policy, action, control, context, prompt, cross-embodiment</b>는 robotics 의미를 보존하도록 혼합 표기한다.</li><li><b>subgoal image, episode metadata, world model</b>은 모델 구성요소의 대응 관계가 흐려지지 않도록 원형을 유지한다.</li><li>모델명·데이터셋명·metric·수치·변수는 원문 표기를 보존한다.</li><li>수식은 Unicode/ASCII로 재작성하고, 표·algorithm은 HTML 요소로 재구성한다.</li><li>본문 인라인 citation 번호는 제거하고 참고문헌 112개는 영문 제목을 유지한다.</li></ul>
{teaser}
'''
final=front+body+video_appendix()+'</div></body></html>'
(BASE/'translation.html').write_text(final)
print('wrote', BASE/'translation.html', 'chars', len(final))
print('figures', len(re.findall(r'data-figure="', final)), 'equations', len(re.findall(r'class="equation"', final)), 'tables', len(re.findall(r'<table', final)), 'videos', len(re.findall(r'>레포 사본</a>', final)))
