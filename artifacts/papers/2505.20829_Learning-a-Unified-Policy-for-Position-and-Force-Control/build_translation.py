#!/usr/bin/env python3
"""Assemble the complete Korean translation for arXiv:2505.20829.

The script deliberately builds semantic HTML (rather than embedding page images),
keeps every translated paragraph, reconstructs canonical figures/tables/equations,
and resolves source references and bibliography citations.
"""
from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path
from typing import Dict, List

import markdown
from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parent
TRANS = ROOT / "translations"
FIG = ROOT / "figures" / "source"
ASSETS = ROOT / "assets"
SOURCE = ROOT / "source"
PARTS = ["part1a.md", "part1b.md", "part2.md", "part3a.md", "part3b.md", "part3c.md"]
TITLE = "Learning a Unified Policy for Position and Force Control in Legged Loco-Manipulation"
AUTHORS = "Peiyuan Zhi, Peiyang Li, Jianqin Yin, Baoxiong Jia, Siyuan Huang"

FIGURES = {
    "fig:teaser": ("1", "teaser_lpy.png", "우리는 다족 로봇을 위한 통합 force-position policy를 제시한다. 이 policy는 position 추종, force 인가, compliant 상호작용을 포함한 다양한 loco-manipulation 동작을 가능하게 한다(상단). 모방학습 데이터 수집에 사용할 때 policy가 학습한 내부 force 추정기는 force-aware 시연을 제공하여, 외부 force 센서 없이 contact-rich 과제의 모델 성능을 향상한다(중단). 사족보행 로봇과 휴머노이드 로봇에서 얻은 결과는 policy의 범용성과 강건성을 입증한다(하단)."),
    "fig:method:model": ("2", "pipeline_v2.png", None),
    "fig:unified_experiment": ("3", "unified_experiment.png", None),
    "fig:imitation": ("4", "exp_il.png", None),
    "fig:skills": ("5", "demo_v5.png", None),
    # The main-paper figure counter ends at 5; the appendix changes the
    # printed format to A.<counter> without resetting it (source PDF pp. 13–16).
    "fig:hardware": ("A.6", None, None),
    "fig:reward_curve": ("A.7", "reward.png", None),
    "fig:open_drawer": ("A.8", "open_drawer.png", None),
    "fig:real_pos_force": ("A.9", None, None),
}
TABLES = {
    "tab:method:rewards": "A.1",
    "tab:method:radomization": "A.2",
    "tab:rebuttal_il_performance": "A.3",
}
EQUATIONS = {
    "eq:impedance_general": ("1", "F = K(x − x_des) + D(ẋ − ẋ_des) + M(ẍ − ẍ_des)"),
    "eq:pos_force_target": ("2", "x_target = x_cmd + [F_ext + (F_cmd − F_react)] / K"),
    "eq:base_simplification": ("3", "F_base = D(ẋ_base − ẋ_base,des) = D(v_base − v_base,des)"),
    "eq:base_pos_force": ("4", "v_base,target = v_base,cmd + [F_base,ext + (F_base,cmd − F_base,react)] / D"),
    "eq:observation": ("5", "o_t = [g_t^base, ω_t^base, q_t, q̇_t, a_(t−1), c_t^cmd, θ_t^feet]"),
    "eq:pos_control": ("A.1", "x_target = x_cmd"),
    "eq:force_control": ("A.2", "x_target = x_cmd + (F_cmd − F_react) / K"),
    "eq:impedance_control": ("A.3", "x_target = x_cmd + F_ext / K"),
    "eq:force_tracking": ("A.4", "Δx_cmd = F_ext / K"),
}
SECTIONS = {
    "sec:intro": ("section-1", "1절"), "sec:method": ("section-3", "3절"),
    "sec:method:formulation": ("section-3-1", "3.1절"), "sec:method:base_formulation": ("section-3-1", "3.1절"),
    "sec:learning": ("section-3-2", "3.2절"), "sec:learning:policy_design": ("section-3-2", "3.2절"),
    "sec:learning:policy_learning": ("section-3-2", "3.2절"), "sec:learning:imitation": ("section-3-3", "3.3절"),
    "sec:exp:imitation": ("section-4-2", "4.2절"), "sec:appendix:formulation": ("appendix-a", "부록 A"),
    "sec:appendix:teleop_details": ("appendix-b", "부록 B"), "sec:appendix:rl_training_details": ("appendix-c", "부록 C"),
    "sec:appendix:cmd_details": ("appendix-c-1", "부록 C.1"), "sec:appendix:il_training_details": ("appendix-d", "부록 D"),
    "sec:appendix:real_word_force_control_experiment": ("appendix-e", "부록 E"),
}


def parse_bbl() -> List[dict]:
    text = (SOURCE / "main.bbl").read_text(encoding="utf-8")
    chunks = re.split(r"(?=\\bibitem\[)", text)[1:]
    refs = []
    for i, chunk in enumerate(chunks, 1):
        m = re.match(r"\\bibitem\[([^]]+)\]\{([^}]+)\}\s*(.*)", chunk, re.S)
        if not m:
            continue
        label, key, body = m.groups()
        year_m = re.search(r"\((\d{4})\)", label)
        year = year_m.group(1) if year_m else (re.findall(r"\b(19\d{2}|20\d{2})\b", body) or [""])[-1]
        short_label = label.split("(", 1)[0].replace("~", " ").strip()
        first = re.split(r"\s+(?:et al\.|and)(?:\s|$)", short_label)[0].strip()
        title_m = re.search(r"\\newblock\s+(.+?)\n", body)
        title = title_m.group(1).strip().rstrip(".") if title_m else "제목 정보 없음"
        title = latex_plain(title)
        full = re.sub(r"\\newblock\s*", " ", body)
        full = re.sub(r"\\(?:emph|url)\{\{([^{}]*)\}\}", r"\1", full)
        full = re.sub(r"\\(?:emph|url)\{([^{}]*)\}", r"\1", full)
        full = re.sub(r"\\end\{thebibliography\}.*$", "", full, flags=re.S)
        full = re.sub(r"\\penalty0", "", full)
        refs.append({"number": i, "key": key, "author": first, "year": year,
                     "title": title, "full": latex_plain(full)})
    if len(refs) != 50:
        raise RuntimeError(f"main.bbl에서 참고문헌 50개가 아니라 {len(refs)}개를 파싱했습니다")
    return refs


def latex_plain(s: str) -> str:
    """Turn small inline LaTeX fragments into readable Unicode/plain text."""
    # Common TeX accents in author names.
    for old, new in [(r'\"a', 'ä'), (r'\"A', 'Ä'), (r'\"o', 'ö'), (r'\"u', 'ü')]:
        s = s.replace(old, new)
    replacements = {
        r"\%": "%", r"\&": "&", r"\,": " ", r"\;": " ", r"\quad": " ",
        r"\sim": "약 ", r"\pi": "π", r"\omega": "ω", r"\theta": "θ", r"\phi": "φ",
        r"\Delta": "Δ", r"\perp": "⊥", r"\in": "∈", r"\mathbb{R}": "ℝ",
        r"\times": "×", r"\leq": "≤", r"\geq": "≥", r"\lvert": "‖", r"\rvert": "‖",
    }
    for old, new in replacements.items():
        s = s.replace(old, new)
    s = re.sub(r"\\(?:mathbf|boldsymbol|mathrm|textit|textbf|texttt|emph|operatorname|mathds|mathbb)\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\(?:text|rm)\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"(\1)/(\2)", s)
    s = re.sub(r"\\exp\{([^{}]*)\}", r"exp(\1)", s)
    s = re.sub(r"\\sum_\{([^{}]+)\}", r"Σ[\1]", s)
    s = re.sub(r"\\ddot\{([^{}]+)\}", r"d²(\1)/dt²", s)
    s = re.sub(r"\\dot\{([^{}]+)\}", r"d(\1)/dt", s)
    s = re.sub(r"\^\{([^{}]+)\}", r"^(\1)", s)
    s = re.sub(r"_\{([^{}]+)\}", r"_(\1)", s)
    s = s.replace(r"\|", " or ").replace("\\", "")
    s = s.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", s).strip()


def equation_html(key: str) -> str:
    num, formula = EQUATIONS[key]
    return f'<pre class="equation" id="equation-{num.replace(".", "-")}" data-equation="{num}" data-source-label="{key}"><code>{html.escape(formula)}</code><span class="eqno">({num})</span></pre>'


def normalize_fragments() -> str:
    parts = [(TRANS / p).read_text(encoding="utf-8") for p in PARTS]
    text = "\n\n".join(parts)
    text = re.sub(r"^source:.*$|^<!--\s*source:.*?-->\s*$", "", text, flags=re.M)

    # Correct the active hierarchy to main sections 1–6 and appendices A–E.
    heading_map = {
        "## 통합 force-position control policy 학습": "### 3.2 통합 Force-Position Control Policy 학습",
        "## Force-aware imitation learning": "### 3.3 Force-aware 모방학습",
        "# 실험": "## 4. 실험", "## Force 및 position 명령 추종": "### 4.1 Force 및 Position 명령 추종",
        "## Force-aware 모방학습": "### 4.2 Force-aware 모방학습", "## 기본 manipulation policy": "### 4.3 기본 Manipulation Policy",
        "## 서로 다른 embodiment에서의 성능": "### 4.4 서로 다른 Embodiment에서의 성능",
        "# 결론": "## 5. 결론", "# 한계 및 향후 연구": "## 6. 한계 및 향후 연구",
        "# 문제 정식화": "## 부록 A. 문제 정식화", "# 하드웨어 설정 및 Teleoperation 시스템": "## 부록 B. 하드웨어 설정 및 Teleoperation 시스템",
        "# Reinforcement learning을 사용한 Policy 학습의 세부사항": "## 부록 C. Reinforcement Learning을 사용한 Policy 학습의 세부사항",
        "## 입력 명령 및 외란 Force": "### C.1 입력 명령 및 외란 Force", "## Reward 및 Domain Randomization": "### C.2 Reward 및 Domain Randomization",
        "## 월드 정렬 End-Effector Position 추정": "### C.3 월드 정렬 End-Effector Position 추정",
        "## Policy 학습에 관한 추가 분석": "### C.4 Policy 학습에 관한 추가 분석", "## Motor Gain의 영향": "### C.5 Motor Gain의 영향",
        "## Sim-to-Real Gap 및 Force 추정 Robustness": "### C.6 Sim-to-Real Gap 및 Force 추정 Robustness",
        "# Force-aware 모방학습 Policy의 세부사항": "## 부록 D. Force-aware 모방학습 Policy의 세부사항",
        "# X축 및 Y축 방향의 Force 추정 정확도 평가": "## 부록 E. X축 및 Y축 방향의 Force 추정 정확도 평가",
    }
    # Context-sensitive duplicate heading in part1b, then global map.
    text = text.replace("## 통합 force-position control policy 학습", heading_map["## 통합 force-position control policy 학습"])
    text = text.replace("## Force-aware imitation learning\n", "### 3.3 Force-aware 모방학습\n", 1)
    for old, new in heading_map.items():
        if old != "## 통합 force-position control policy 학습":
            text = text.replace(old, new)

    # Hardware's two source panels are one canonical Figure A.6.
    hardware_pat = r"\[\[FIGURE:fig:b2z1_hardware.*?\*\*하드웨어 설정 및 teleoperation 시스템\.\*\* \[\[REF:fig:hardware\]\]"
    text = re.sub(hardware_pat, "[[FIGURE:fig:hardware|combined|wide]]\n\n**하드웨어 설정 및 teleoperation 시스템.** (a) Z1 arm을 장착한 Unitree B2 로봇, wireless controller, 시각 입력용 RealSense camera 두 대. (b) MuJoCo AR 앱과 iPhone을 사용하는 position-control teleoperation.", text, flags=re.S)

    # Replace the nine numbered source equations with stable semantic slots.
    replacements = [
        (r"𝐅 = K\(𝐱 − 𝐱\^des\).*?\[\[REF:eq:impedance_general\]\]", "[[EQUATION:eq:impedance_general]]"),
        (r"𝐱\^target = 𝐱\^cmd \+ \[𝐅\^ext \+ \(𝐅\^cmd − 𝐅\^react\)\] / K\..*?\[\[REF:eq:pos_force_target\]\]", "[[EQUATION:eq:pos_force_target]]"),
        (r"F_base = D\(ẋ_base − ẋ_base\^des\) = D\(v_base − v_base\^des\)\.\s*\(1\)", "[[EQUATION:eq:base_simplification]]"),
        (r"v_base\^target = v_base\^cmd \+ \[F_base\^ext \+ \(F_base\^cmd − F_base\^react\)\] / D\.\s*\(2\)", "[[EQUATION:eq:base_pos_force]]"),
        (r"o_t = \[g_t\^base, ω_t\^base, q_t, q̇_t, a_\{t−1\}, c_t\^cmd, θ_t\^feet\]\.", "[[EQUATION:eq:observation]]"),
    ]
    for pat, val in replacements:
        # Each canonical main equation occurs once; count=1 prevents the
        # unnumbered simplified impedance expression from spanning forward.
        text = re.sub(pat, val, text, count=1, flags=re.S)
    app_eq = ["eq:pos_control", "eq:force_control", "eq:impedance_control", "eq:force_tracking"]
    for key in app_eq:
        text = re.sub(r"\$\$.*?\$\$\s*\n\s*\[\[REF:" + re.escape(key) + r"\]\]", f"[[EQUATION:{key}]]", text, count=1, flags=re.S)

    # Convert remaining inline math to readable text, retaining code/task backticks.
    text = re.sub(r"\$\$([^$]+)\$\$", lambda m: f'<code class="inline-math">{html.escape(latex_plain(m.group(1)))}</code>', text, flags=re.S)
    text = re.sub(r"\$([^$\n]+)\$", lambda m: f'<code class="inline-math">{html.escape(latex_plain(m.group(1)))}</code>', text)
    text = re.sub(r"\\\((.*?)\\\)", lambda m: f'<code class="inline-math">{html.escape(latex_plain(m.group(1)))}</code>', text)
    return text


def resolve_tokens(text: str, refs: List[dict]) -> str:
    ref_by_key = {r["key"]: r for r in refs}

    def cite(m):
        links = []
        for key in m.group(1).split(","):
            r = ref_by_key.get(key.strip())
            if not r:
                raise KeyError(f"알 수 없는 인용 키: {key}")
            links.append(f'<a class="citation" href="#ref-{r["number"]}" title="{html.escape(r["author"] + " " + r["year"])}">{r["number"]}</a>')
        return "[" + ", ".join(links) + "]"
    text = re.sub(r"\[\[CITE:([^]]+)\]\]", cite, text)

    def source_ref(m):
        key = m.group(1)
        # Source subfigure labels both resolve to the combined canonical Figure A.6.
        if key in {"fig:b2z1_hardware", "fig:iphone_tele"}:
            return f'<a class="xref" href="#fig-A.6" data-source-ref="{key}">그림 A.6</a>'
        if key in FIGURES:
            n = FIGURES[key][0]; return f'<a class="xref" href="#fig-{n}" data-source-ref="{key}">그림 {n}</a>'
        if key in TABLES:
            n = TABLES[key]; return f'<a class="xref" href="#table-{n.replace(".", "-")}" data-source-ref="{key}">표 {n}</a>'
        if key in EQUATIONS:
            n = EQUATIONS[key][0]; return f'<a class="xref" href="#equation-{n.replace(".", "-")}" data-source-ref="{key}">식 ({n})</a>'
        if key in SECTIONS:
            ident, label = SECTIONS[key]; return f'<a class="xref" href="#{ident}" data-source-ref="{key}">{label}</a>'
        raise KeyError(f"알 수 없는 참조: {key}")
    return re.sub(r"\[\[REF:([^]]+)\]\]", source_ref, text)


def build_body(text: str) -> BeautifulSoup:
    # Tokens become inert custom tags, then are expanded in the parsed DOM.
    text = re.sub(r"\[\[FIGURE:([^|]+)\|[^|]+\|[^]]+\]\]", r'<figure-slot data-key="\1"></figure-slot>', text)
    text = re.sub(r"\[\[TABLE:([^]]+)\]\]", r'<table-slot data-key="\1"></table-slot>', text)
    text = re.sub(r"\[\[EQUATION:([^]]+)\]\]", r'<equation-slot data-key="\1"></equation-slot>', text)
    rendered = markdown.markdown(text, extensions=["tables", "sane_lists"])
    soup = BeautifulSoup(f"<div>{rendered}</div>", "html.parser")

    # Heading IDs and full-width section styling.
    heading_ids = {
        "1. 서론":"section-1", "2. 관련 연구":"section-2", "3. 방법":"section-3",
        "3.1 Force 및 Position Control을 위한 통합 정식화":"section-3-1",
        "3.2 통합 Force-Position Control Policy 학습":"section-3-2", "3.3 Force-aware 모방학습":"section-3-3",
        "4. 실험":"section-4", "4.1 Force 및 Position 명령 추종":"section-4-1", "4.2 Force-aware 모방학습":"section-4-2",
        "5. 결론":"section-5", "6. 한계 및 향후 연구":"section-6", "부록 A. 문제 정식화":"appendix-a", "부록 B. 하드웨어 설정 및 Teleoperation 시스템":"appendix-b",
        "부록 C. Reinforcement Learning을 사용한 Policy 학습의 세부사항":"appendix-c", "C.1 입력 명령 및 외란 Force":"appendix-c-1",
        "부록 D. Force-aware 모방학습 Policy의 세부사항":"appendix-d", "부록 E. X축 및 Y축 방향의 Force 추정 정확도 평가":"appendix-e",
    }
    for h in soup.find_all(re.compile("^h[1-6]$")):
        h["id"] = heading_ids.get(h.get_text(" ", strip=True), "heading-" + str(len(soup.select('[id^="heading-"]')) + 1))
        if h.name == "h2": h["class"] = ["section"]

    # Equations.
    for slot in list(soup.find_all("equation-slot")):
        eq = BeautifulSoup(equation_html(str(slot["data-key"])), "html.parser").select_one(".equation")
        slot.replace_with(eq)

    # Figures: the translated caption is the immediately following paragraph.
    for slot in list(soup.find_all("figure-slot")):
        key = slot["data-key"]
        num, filename, forced_caption = FIGURES[key]
        anchor = slot.parent if slot.parent and slot.parent.name == "p" else slot
        capnode = anchor.find_next_sibling("p")
        caption = forced_caption or (capnode.get_text(" ", strip=True) if capnode else "")
        if capnode and not forced_caption:
            capnode.extract()
        fig = soup.new_tag("figure", id=f"fig-{num}")
        fig["data-figure"] = num; fig["class"] = "fig-wide"
        if key == "fig:hardware":
            fig["data-source-labels"] = "fig:b2z1_hardware fig:iphone_tele fig:hardware"
        elif key == "fig:real_pos_force":
            fig["data-source-labels"] = "fig:real_pos_force: pos_est|fig:real_pos_force: pos_tracking_woforce|fig:real_pos_force"
        else:
            fig["data-source-label"] = key
        if key == "fig:hardware":
            panels = soup.new_tag("div", attrs={"class":"panel-grid"})
            for src, alt, lab in [("hardware.png", "B2-Z1 로봇 하드웨어", "(a)"), ("iphone_tele.jpg", "iPhone teleoperation", "(b)")]:
                box = soup.new_tag("div"); img = soup.new_tag("img", src=f"figures/source/{src}", alt=alt); box.append(img)
                label = soup.new_tag("span"); label.string=lab; box.append(label); panels.append(box)
            fig.append(panels)
        elif key == "fig:real_pos_force":
            panels = soup.new_tag("div", attrs={"class":"panel-grid"})
            for src, alt, lab in [("y_force_discrete.png", "Y축 force 평가", "Y축"), ("z_force_discrete.png", "Z축 force 평가", "Z축")]:
                box=soup.new_tag("div"); img=soup.new_tag("img",src=f"figures/source/{src}",alt=alt); box.append(img)
                label=soup.new_tag("span"); label.string=lab; box.append(label); panels.append(box)
            fig.append(panels)
        else:
            fig.append(soup.new_tag("img", src=f"figures/source/{filename}", alt=f"그림 {num}"))
        fc = soup.new_tag("figcaption"); b=soup.new_tag("b"); b.string=f"그림 {num}. "; fc.append(b)
        fc.append(BeautifulSoup(caption, "html.parser"))
        if key == "fig:skills":
            note=soup.new_tag("span", attrs={"class":"source-note"}); note.string=" (패널 표기는 원문 표기 (a, d, c, d)를 보존함.)"; fc.append(note)
        fig.append(fc); anchor.replace_with(fig)

    # Tables: marker, caption paragraph, and Markdown table become one entity.
    for slot in list(soup.find_all("table-slot")):
        key=slot["data-key"]; num=TABLES[key]
        anchor = slot.parent if slot.parent and slot.parent.name == "p" else slot
        cap=anchor.find_next_sibling("p"); table=cap.find_next_sibling("table") if cap else anchor.find_next_sibling("table")
        if table is None: raise RuntimeError(f"{key}의 HTML 표를 찾지 못했습니다")
        caption=cap.get_text(" ",strip=True) if cap else ""
        if cap: cap.extract()
        wrap=soup.new_tag("div", id=f"table-{num.replace('.', '-')}", attrs={"class":"table-entity wide","data-table":num,"data-source-label":key})
        c=soup.new_tag("div",attrs={"class":"table-caption"}); b=soup.new_tag("b"); b.string=f"표 {num}. "; c.append(b); c.append(caption); wrap.append(c)
        table.extract(); table["class"]="source-table"; wrap.append(table); anchor.replace_with(wrap)

    # Plain residual math/code is readable, never raw LaTeX.
    for node in soup.find_all(string=True):
        if node.parent and node.parent.name not in {"script", "style"} and "math" not in node.parent.get("class", []) and "\\" in str(node):
            node.replace_with(latex_plain(str(node)))
    return soup


CSS = r"""
@page { size:A4; margin:14mm 13mm 15mm; }
*{box-sizing:border-box} html{-webkit-print-color-adjust:exact;print-color-adjust:exact;scroll-behavior:smooth}
body{margin:0;color:#151515;font-family:"Noto Sans KR","Apple SD Gothic Neo",sans-serif;font-size:9.3pt;line-height:1.58}
a{color:#174f86;text-decoration:none}.cover{height:250mm;min-height:0;position:relative;padding:12mm 12mm 10mm 19mm;page-break-after:always;border-left:6px solid #111;display:flex;flex-direction:column;justify-content:center}
.cover h1{font-size:29pt;line-height:1.16;margin:0 0 5mm;border-bottom:3px solid #111;padding-bottom:5mm}.cover .ko{font-size:15pt;font-weight:800}.meta{margin-top:12mm;line-height:1.9}.cover-note{color:#666;margin-top:8mm;max-width:155mm}.body{column-count:2;column-gap:7mm;text-align:justify}.doc-title,.frontmatter,.teaser,.toc{column-span:all}.toc{border:1px solid #bbb;background:#fafafa;padding:3mm 5mm;margin:3mm 0 5mm}.toc h2{margin:0 0 2mm}.toc ol{columns:2}.toc li.sub{margin-left:4mm;font-size:8.5pt}.doc-title{font-size:18pt;line-height:1.25;border-bottom:2px solid #111;margin:0 0 4mm;padding-bottom:3mm}.frontmatter{columns:2;column-gap:7mm;margin-bottom:3mm}.frontmatter p{margin:0 0 1mm}.body p{margin:0 0 2.3mm}h2.section{column-span:all;font-size:15pt;margin:5mm 0 2.5mm;padding:2mm 0;border-top:1px solid #aaa;border-bottom:1px solid #aaa;break-after:avoid}h3{font-size:11.2pt;margin:3mm 0 1mm;break-after:avoid}h4{font-size:9.6pt;margin:2mm 0 .5mm}ul,ol{padding-left:5mm;margin:1mm 0 2mm}li{margin-bottom:1mm}figure{margin:3mm 0;text-align:center;break-inside:avoid}figure.fig-wide,.table-entity.wide,.video-appendix,.references{column-span:all}figure img{max-width:100%;max-height:210mm;object-fit:contain}figcaption,.table-caption{font-size:8.4pt;color:#444;margin-top:1mm}.source-note{font-size:7.7pt;color:#777}.panel-grid{display:grid;grid-template-columns:1fr 1fr;gap:3mm}.panel-grid div{display:flex;flex-direction:column;align-items:center;font-size:8pt;color:#555}.equation{position:relative;font-family:"DejaVu Sans Mono",monospace;background:#f5f6f7;border:1px solid #ddd;padding:2.5mm 12mm 2.5mm 3mm;white-space:pre-wrap;break-inside:avoid;text-align:center}.equation code{font:inherit}.eqno{position:absolute;right:3mm}table{width:100%;border-collapse:collapse;font-size:8pt;margin:1mm 0 3mm;break-inside:avoid}th,td{border:.6pt solid #333;padding:1.2mm;text-align:center;overflow-wrap:anywhere}th{background:#e9ecef}.table-entity{break-inside:avoid;margin:3mm 0}.table-caption{text-align:center;margin-bottom:1mm}.citation{font-size:8pt}.video-appendix{break-before:page}.video-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:4mm}.video-card{border:1px solid #ccc;border-radius:3px;padding:2mm;margin:0}.video-card img{width:100%;aspect-ratio:16/9;object-fit:cover}.video-links{font-size:8pt}.badge{background:#174f86;color:white;border-radius:2px;padding:0 1mm}.refs{columns:2;column-gap:7mm;font-size:7.4pt;line-height:1.35;padding-left:6mm}.refs li{break-inside:avoid;margin-bottom:.8mm}code{font-family:"DejaVu Sans Mono",monospace;background:#f1f1f1;padding:0 .5mm}@media screen{body{max-width:210mm;margin:auto;padding:8mm;box-shadow:0 0 8px #bbb}.cover{min-height:260mm}}@media print{body{padding:0}.cover{height:250mm;min-height:0}a{color:#111}.video-card{break-inside:avoid}.video-links{display:none}}
@media screen and (max-width:760px){body{padding:4mm;box-shadow:none}.cover{min-height:auto;padding:12mm 6mm}.cover h1{font-size:21pt}.body{column-count:1}.frontmatter{columns:1}.toc ol,.refs{columns:1}.video-grid,.panel-grid{grid-template-columns:1fr}figure.fig-wide,.table-entity.wide,.video-appendix,.references{column-span:none}table{display:block;overflow-x:auto}}
"""


def video_section(videos: dict) -> str:
    # Labels are grounded in the grouping and labels on the official project page.
    labels = {
        "Corl_PF_3min": "논문의 통합 force-position policy, 모방학습, cross-embodiment 결과를 묶은 전체 개요",
        "Corl_PF_web2": "Force control: 명령 force를 따라 payload를 지지하는 동작",
        "Corl_PF_web3": "Force tracking: 외력에 따라 end-effector가 이동하는 동작",
        "Corl_PF_web4": "Impedance control: 외란에 compliant하게 반응하는 동작",
        "Corl_PF_web5": "Base force tracking: base에 가해진 밀기에 반응하는 사족보행 로봇",
        "Corl_PF_web7": "Force control: 휴머노이드 embodiment의 force 제어",
        "Corl_PF_web6": "Base force tracking: 휴머노이드 embodiment의 외력 대응",
        "Corl_PF_web8": "Force-aware 모방학습 결과 장면 1",
        "Corl_PF_web9": "Force-aware 모방학습 결과 장면 2",
        "Corl_PF_web1": "Cross-embodiment 실험 장면",
        "Corl_PF_web11_1": "Whole-body manipulation task 장면 1",
        "Corl_PF_web11_2": "Whole-body manipulation task 장면 2",
        "Corl_PF_web11_3": "Whole-body manipulation task 장면 3",
        "Corl_PF_web11_4": "Whole-body manipulation task 장면 4",
    }
    cards=[]
    for i,a in enumerate(videos["assets"],1):
        stem = Path(a["local"]).name.split("-")[0]
        scene = labels[stem]
        cards.append(f'''<figure class="video-card" data-video="{i}"><a href="{html.escape(a['local'])}"><img src="{html.escape(a['thumbnail'])}" alt="{html.escape(scene)}"></a><figcaption><b>보충 영상 {i}. {html.escape(scene)}</b> · {a['duration_s']:.2f}초 · {a['width']}×{a['height']}<span class="video-links"><span class="badge">VIDEO</span> <a href="{html.escape(a['local'])}">로컬 영상</a> · <a href="{html.escape(a['url'])}">원본 링크</a></span></figcaption></figure>''')
    return '<section class="video-appendix" id="videos"><h2 class="section">보충 영상 부록</h2><p>프로젝트 페이지에서 제공하는 보충 영상 14개를 모두 수록했다. 장면 설명은 공식 프로젝트 페이지의 그룹 및 표제를 따른다.</p><div class="video-grid">'+''.join(cards)+'</div></section>'


def main_tables() -> str:
    """Six accessible tables reconstructed only from values in active source prose."""
    specs = [
      ("1", "Policy의 관측, 명령 및 action 구성", ["구분","원문 구성"], [["관측","base orientation·angular velocity, joint position·velocity, previous action, command, feet clock timing"],["명령","base velocity, end-effector position/force, base force"],["Action","default pose에 더하는 residual; PD joint-position target"]]),
      ("2", "학습 중 입력 명령과 외란 force 범위", ["항목","범위"], [["End-effector 반경 r","0.35–0.85 m"],["각도 θ / φ","−0.4π–0.4π / −0.6π–0.6π rad"],["End-effector / base force","각 축 −60–60 N"],["Base velocity vx / vy / ωz","−0.8–0.8 / −0.6–0.6 m/s / −0.8–0.8 rad/s"]]),
      ("3", "학습 설정", ["항목","설정"], [["RL","PPO, Isaac Gym, 4096 parallel environments, 2-stage curriculum"],["Observation history","H = 32"],["Wipe-blackboard IL","50 trajectories, 30k steps"],["다른 세 IL 과제","과제당 30 episodes, 20k steps"]]),
      ("4", "Force 및 position control 평가 프로토콜", ["평가","원문 설정"], [["Simulation position tracking","6000-step rollouts; 전체 training workspace"],["Real force control","0–60 N; 5 end-effector positions"],["Y/Z hardware 평가","40 N 이내"],["Force estimation","6 discrete levels"]]),
      ("5", "Force-aware 모방학습 과제와 평가", ["과제","시연 수","학습","평가"], [["wipe-blackboard","50 trajectories","30k steps","50 trials, ≤1000 steps"],["open-cabinet","30 episodes","20k steps","50 trials, ≤1000 steps"],["close-cabinet","30 episodes","20k steps","50 trials, ≤1000 steps"],["open-drawer-occlusion","30 episodes","20k steps","50 trials, ≤1000 steps"]]),
      ("6", "본문에 보고된 주요 정량 결과", ["결과","값"], [["4개 IL 과제 평균 성공률 향상","약 39.5%"],["Position tracking error","대부분 0.1 m 이내"],["Position estimation error","모든 축 0.05 m 이내"],["Real force-control average error","10 N 이내"],["6단계 force-estimation error","5–10 N"],["Occluded drawer: baseline / ours","0.30 / 0.76"]]),
    ]
    entities=[]
    for n,cap,heads,rows in specs:
        th=''.join(f'<th>{html.escape(x)}</th>' for x in heads)
        trs=''.join('<tr>'+''.join(f'<td>{html.escape(x)}</td>' for x in row)+'</tr>' for row in rows)
        entities.append(f'<div class="table-entity wide" id="table-{n}" data-table="{n}" data-source-ref="active-prose"><div class="table-caption"><b>표 {n}. </b>{cap}</div><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>')
    return '<section class="source-tables" id="main-tables"><h2 class="section">본문 데이터 표</h2><p>원문의 능동 본문에 서술된 설정과 결과를 값 변경 없이 접근 가능한 표로 재구성했다.</p>'+''.join(entities)+'</section>'


def main() -> None:
    refs=parse_bbl(); videos=json.loads((ASSETS/"videos.json").read_text(encoding="utf-8"))
    text=resolve_tokens(normalize_fragments(),refs)
    soup=build_body(text)
    # teaser is canonical Figure 1 and belongs in the front matter.
    teaser_num, teaser_file, teaser_cap=FIGURES["fig:teaser"]
    teaser=f'<figure class="fig-wide teaser" id="fig-1" data-figure="1" data-source-label="fig:teaser"><img src="figures/source/{teaser_file}" alt="통합 force-position policy 개요"><figcaption><b>그림 1. </b>{teaser_cap}</figcaption></figure>'
    ref_html=''.join(f'<li id="ref-{r["number"]}">{html.escape(r["full"])}</li>' for r in refs)
    bibliography=f'<section class="references" id="references"><h2 class="section">참고문헌</h2><p>참고문헌 50개는 원문의 main.bbl 순서와 전체 서지 내용을 따른다.</p><ol class="refs">{ref_html}</ol></section>'
    body_inner=soup.div.decode_contents()
    toc_items=[]
    for h in soup.select("h2[id], h3[id]"):
        cls="sub" if h.name=="h3" else "main"
        toc_items.append(f'<li class="{cls}"><a href="#{h["id"]}">{html.escape(h.get_text(" ",strip=True))}</a></li>')
    toc='<nav class="toc" id="toc"><h2>목차</h2><ol>'+''.join(toc_items)+'</ol></nav>'
    today=date.today().isoformat()
    doc=f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{TITLE} — 한국어 전문 번역</title><style>{CSS}</style></head><body>
<section class="cover"><h1>{TITLE}</h1><div class="ko">다족 Loco-Manipulation에서 Position 및 Force Control을 위한 통합 Policy 학습<br>한국어 전문 번역</div><div class="meta"><b>저자</b> Peiyuan Zhi<sup>1,2,*</sup>, Peiyang Li<sup>1,3,*</sup>, Jianqin Yin<sup>3</sup>, Baoxiong Jia<sup>1,2,†</sup>, Siyuan Huang<sup>1,2,†</sup><br><b>학회</b> Conference on Robot Learning (CoRL 2025) · <b>arXiv</b> 2505.20829v2<br><b>최초 공개</b> 2025-05-27 · <b>최종 수정</b> 2025-10-04 · <b>분류</b> cs.RO<br><b>원문</b> <a href="https://arxiv.org/abs/2505.20829v2">arxiv.org/abs/2505.20829v2</a><br><b>프로젝트</b> <a href="https://unified-force.github.io/">unified-force.github.io</a><br><b>번역 생성일</b> {today}</div><p class="cover-note">원문의 능동 본문을 생략 없이 한국어로 재구성했다. 그림은 source-native 자산, 표는 접근 가능한 HTML 표, 수식은 인쇄 안전형 Unicode 표기로 제시한다.</p></section>
<main class="body"><h1 class="doc-title">다족 Loco-Manipulation에서 Position 및 Force Control을 위한 통합 Policy 학습<br><span>{TITLE}</span></h1><div class="frontmatter"><p><b>저자:</b> Peiyuan Zhi<sup>1,2,*</sup>, Peiyang Li<sup>1,3,*</sup>, Jianqin Yin<sup>3</sup>, Baoxiong Jia<sup>1,2,†</sup>, Siyuan Huang<sup>1,2,†</sup></p><p><b>소속 1:</b> State Key Laboratory of General Artificial Intelligence, BIGAI<br><b>소속 2:</b> Joint Laboratory of Embodied AI and Humanoid Robots, BIGAI &amp; UniTree Robotics<br><b>소속 3:</b> Beijing University of Posts and Telecommunications<br><b>*</b> 동등 기여. <b>†</b> 교신저자.</p><p><b>번역 기준:</b> arXiv 2505.20829v2; 공개 2025-05-27, 수정 2025-10-04</p></div>{toc}{teaser}{body_inner}{video_section(videos)}{bibliography}</main></body></html>'''
    out=ROOT/"translation.html"; out.write_text(doc,encoding="utf-8")

    citation_map={r["key"]:{"number":r["number"],"author":r["author"],"year":r["year"],"title":r["title"],"id":f"ref-{r['number']}"} for r in refs}
    (ROOT/"citation_map.json").write_text(json.dumps(citation_map,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    final=BeautifulSoup(doc,"html.parser")
    counts={"figures":len(final.select("[data-figure]")),"tables":len(final.select("[data-table]")),"equations":len(final.select(".equation[data-equation]")),"references":len(final.select("ol.refs > li")),"inline_citations":len(final.select("a.citation")),"videos":len(final.select("[data-video]"))}
    local_paths=[]
    for tag in final.select("img[src], a[href]"):
        val=tag.get("src") or tag.get("href")
        if val and not re.match(r"(?:https?:|#|mailto:)",val): local_paths.append(val)
    missing=sorted({p for p in local_paths if not (ROOT/p).exists()})
    visible_tree=BeautifulSoup(doc,"html.parser")
    for tag in visible_tree.select("script, style"): tag.decompose()
    visible=visible_tree.get_text(" ",strip=True)
    raw_latex=sorted(set(re.findall(r"\\[A-Za-z]+",visible)))
    unresolved=re.findall(r"\[\[(?:CITE|REF|FIGURE|TABLE|EQUATION):",doc)
    ids=[str(tag["id"]) for tag in final.select("[id]")]
    duplicate_ids=sorted({x for x in ids if ids.count(x)>1})
    expected={"figures":9,"tables":3,"equations":9,"references":50,"videos":14}
    errors=[]
    for k,v in expected.items():
        if counts[k]!=v: errors.append(f"{k}: expected {v}, got {counts[k]}")
    if missing: errors.append("missing local assets: "+", ".join(missing))
    if raw_latex: errors.append("raw visible LaTeX: "+", ".join(raw_latex))
    if unresolved: errors.append(f"unresolved tokens: {len(unresolved)}")
    if duplicate_ids: errors.append("duplicate ids: "+", ".join(duplicate_ids))
    if errors: raise RuntimeError("Self-check failed:\n- " + "\n- ".join(errors))

    figure_nos=["1","2","3","4","5","A.6","A.7","A.8","A.9"]
    table_nos=["A.1","A.2","A.3"]
    equation_nos=["1","2","3","4","5","A.1","A.2","A.3","A.4"]
    manifest={"arxiv_id":"2505.20829","title":TITLE,"language":"ko","generated":today,"source_fragments":PARTS,"outputs":["translation.html","manifest.json","citation_map.json","README.md"],"figures":[{"no":n} for n in figure_nos],"tables":[{"no":n} for n in table_nos],"display_equations":9,"canonical":{"figures":figure_nos,"tables":table_nos,"equations":equation_nos},"counts":counts,"self_check":{"missing_local_paths":missing,"raw_visible_latex":raw_latex,"unresolved_tokens":len(unresolved),"duplicate_ids":duplicate_ids,"status":"passed"}}
    (ROOT/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    readme=f'''# arXiv 2505.20829 한국어 전문 번역\n\n`build_translation.py`가 6개 번역 fragment와 source-native 자산을 조립해 `translation.html`을 생성합니다.\n\n## 재생성\n\n```bash\npython3 build_translation.py\n```\n\n## 생성물\n\n- `translation.html`: A4 1쪽 표지 + 2단 한국어 학술 레이아웃\n- `manifest.json`: canonical entity와 self-check 결과\n- `citation_map.json`: main.bbl 순서의 50개 인용 매핑\n\n## 검증된 개수\n\n- 그림: {counts['figures']} (1–5, A.6–A.9; 원문은 부록에서 figure counter를 reset하지 않음)\n- 표: {counts['tables']} (A.1–A.3)\n- 수식: {counts['equations']} (1–5, A.1–A.4)\n- 참고문헌: {counts['references']}\n- 본문 인용 링크: {counts['inline_citations']}\n- 보충 영상: {counts['videos']}\n\nSelf-check는 모든 로컬 경로, 미해결 token, 화면에 보이는 raw LaTeX residue도 검사합니다.\n'''
    (ROOT/"README.md").write_text(readme,encoding="utf-8")
    print(json.dumps({"status":"ok","output":str(out),"counts":counts,"bytes":out.stat().st_size},ensure_ascii=False,indent=2))

if __name__=="__main__": main()
