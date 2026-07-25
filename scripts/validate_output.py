#!/usr/bin/env python3
"""번역 산출물이 출력 계약을 지키는지 기계 검증한다 (pymupdf/fitz).

이 스크립트는 SKILL.md의 "출력 계약"을 강제하는 필수 게이트다. 열화 산출물의
전형적 실패(원문 페이지 통 캡처 삽입, 페이지 단위 텍스트 덤프, 표 미재구성,
경어체)를 자동 검출한다.

반드시 uv로 실행한다 (시스템 pip는 PEP 668로 막혀 있음):
    uv run --quiet --with pymupdf python3 validate_output.py <workdir> [--final <최종.pdf>]
    uv run --quiet --with pymupdf python3 validate_output.py --pdf-only <최종.pdf> <원본.pdf>

모드:
  A(작업폴더 검증)  <workdir> [--final <최종.pdf>]
        workdir에서 original.pdf, translation.html, figures/를 찾아 HTML 계약과
        최종 PDF를 검사한다. --final 미지정 시 workdir 안팎에서
        *_ko_translation_layout.pdf / *_paper_translate_ko.pdf 를 glob으로 찾는다.
        manifest.json이 있으면 개수 기준(그림/표/수식)으로, 없으면 휴리스틱으로 검사한다.

  B(PDF 소급 검증)  --pdf-only <최종.pdf> <원본.pdf>
        작업폴더 없이 최종 PDF와 원본 PDF만으로 PDF 검사 항목을 수행한다.

출력: 항목별 [PASS]/[WARN]/[FAIL] 리포트 + 마지막 줄 종합 판정.
FAIL 1개 이상이면 exit code 1, 아니면 0.

manifest.json 스키마:
    {
      "figures": [{"no": "1", "page": 2, "desc": "시스템 개요"}, ...],
      "tables":  [{"no": "1", "page": 5, "desc": "정량 비교"}, ...],
      "display_equations": 7
    }
"""
import glob
import html as _html
import json
import os
import re
import sys
from html.parser import HTMLParser

import fitz  # pymupdf


# ---- 계약 임계값 ---------------------------------------------------------
FORBIDDEN_STRINGS = ["원문 p.", "레이아웃 보존"]  # 페이지 통 캡처/덤프의 흔적
PLACEHOLDER_PATTERNS = [
    "Original English Paper Title",
    "Original Paper Title",
    "First Author",
    "Second Author",
    "VENUE YEAR",
    "0000.00000",
    "YYYY-MM-DD",
    "여기에 초록",
    "여기서부터 실제 내용으로 교체",
    "fig-p01-01.png",
    "fig-p04-01.png",
]
HABNIDA_LIMIT = 15          # "습니다" 출현이 이보다 많으면 경어체 위반 신호
RATIO_FAIL_LOW = 0.5        # 최종/원본 페이지 비율이 이 미만이면 FAIL(누락 의심)
RATIO_FAIL_HIGH = 2.0       # 이 초과면 FAIL(통 캡처로 페이지 폭증 의심)
RATIO_WARN_LOW = 0.7        # ±30% 밖이면 WARN
RATIO_WARN_HIGH = 1.3
IMG_FRAC_HARD = 0.75        # 단일 이미지가 페이지의 이 비율 초과면 무조건 통 캡처
IMG_FRAC_SPARSE = 0.55      # 이 비율 초과 + 본문이 희박하면 통 캡처(캡션만 있는 이미지 페이지)
SPARSE_TEXT_LEN = 300       # 페이지 추출 텍스트가 이보다 짧으면 "본문 없음"으로 본다

# LaTeX 잔재: 수식을 ASCII/유니코드로 변환하지 않고 원문 문법을 노출한 흔적.
# (실사례: `$$ \textrm{GASI}=\mathbb{E}...\tag{3} $$` 가 산출물에 그대로 인쇄됨)
LATEX_REMNANT = re.compile(r"\\[A-Za-z]+|\$\$")
# PDF/LaTeXML 접근성 트리나 machine translation에서 수식이 중복 낭독된 흔적.
# 예: `p_IDM(...) 아래 첨자 ... p_{textrm{textsubscript{IDM}}}(...)`.
# 정상 수식은 ASCII/유니코드 한 벌만 남겨야 한다.
FORMULA_SPEECH_REMNANTS = (
    ("아래 첨자", re.compile(r"아래\s+첨자")),
    ("하위 첨자", re.compile(r"하위\s+첨자")),
    ("위 첨자", re.compile(r"위\s+첨자")),
    ("formulae-sequence", re.compile(r"\bformulae(?:\s+|-)sequence\b", re.IGNORECASE)),
    ("leavevmode", re.compile(r"\bleavevmode\b", re.IGNORECASE)),
    ("textsubscript", re.compile(r"\btextsubscript\b", re.IGNORECASE)),
    ("textrm", re.compile(r"\btextrm\b", re.IGNORECASE)),
    ("similar-to", re.compile(r"\bsimilar(?:\s+|-)to\b", re.IGNORECASE)),
    ("superscript", re.compile(r"\bsuperscript\b", re.IGNORECASE)),
    ("subscript", re.compile(r"\bsubscript\b", re.IGNORECASE)),
)
PDF_STRONG_REMNANT_LABELS = {
    "formulae-sequence", "leavevmode", "textsubscript", "textrm", "similar-to",
}
FORMULA_CONTEXT_SIGNAL = re.compile(r"[=_|{}\\^∑∏±×÷≤≥∈⊆]|[A-Za-z]\s*\([^)]*\)")
MACHINE_TRANSLATION_RESIDUE = (
    ("건강하게 감소", re.compile(r"건강하게\s*감소")),
    ("시각적 영역의 영향력 있는 변화", re.compile(r"시각적\s*영역[\s\S]{0,24}영향력\s*있는\s*변화")),
    ("예측할 수 있다고 예상할 수", re.compile(r"예측할\s*수\s*있다고\s*예상할\s*수")),
    ("제작대를 제작", re.compile(r"제작대(?:를)?\s*제작")),
    ("기술 트리에서는 이를 지나칠 수 없", re.compile(r"기술\s*트리에서는?\s*이를?\s*지나칠\s*수\s*없")),
    ("두 개의 더 좁은 데이터 세트", re.compile(r"두\s*개(?:의)?\s*더\s*좁은\s*데이터\s*세트")),
    (
        "상반된 데이터 분류에 동일한 이름 반복",
        re.compile(
            r"데이터(?:를)?\s*[\"“](?P<label>[^\"”]{1,20})[\"”](?:이라고)?\s*부르"
            r"[\s\S]{0,100}다른\s*모든\s*데이터(?:는|를)?\s*[\"“](?P=label)[\"”]"
        ),
    ),
)
# 인라인 인용 잔존: [12], [3, 4] — 단 '∈ [0,1]' 같은 수식 구간은 오탐이므로 WARN만.
INLINE_CITE = re.compile(r"\[\d{1,3}(?:,\s*\d{1,3})*\]")
CITE_OK_CONTEXT = re.compile(r"[∈±\[\(=,]\s*$")


class Report:
    """항목별 결과를 모으고 종합 판정을 낸다."""

    def __init__(self):
        self.items = []  # (level, msg)

    def add(self, level, msg):
        self.items.append((level, msg))

    def ok(self, msg):
        self.add("PASS", msg)

    def warn(self, msg):
        self.add("WARN", msg)

    def fail(self, msg):
        self.add("FAIL", msg)

    @property
    def failed(self):
        return any(lv == "FAIL" for lv, _ in self.items)

    def print(self):
        for lv, msg in self.items:
            print(f"[{lv}] {msg}")
        n_fail = sum(1 for lv, _ in self.items if lv == "FAIL")
        n_warn = sum(1 for lv, _ in self.items if lv == "WARN")
        print("-" * 72)
        if n_fail:
            print(f"종합 판정: FAIL — 위반 {n_fail}건, 경고 {n_warn}건. "
                  f"위 [FAIL] 항목을 교정하고 재검증하라.")
        elif n_warn:
            print(f"종합 판정: PASS(경고 {n_warn}건) — 위반 없음. "
                  f"[WARN] 항목은 확인 권장이나 완료를 막지는 않는다.")
        else:
            print("종합 판정: PASS — 모든 검사 통과.")


# ---- 공통 유틸 -----------------------------------------------------------
def _pdf_page_count(path):
    d = fitz.open(path)
    n = len(d)
    d.close()
    return n


def _pdf_text(path):
    d = fitz.open(path)
    txt = "".join(pg.get_text() for pg in d)
    d.close()
    return txt


def _count_table_refs(text):
    """원문 텍스트에서 'Table N' 참조 수(표가 존재한다는 신호)."""
    return len(re.findall(r"\bTable\s+\d+", text))


class _VisibleHTMLText(HTMLParser):
    """HTML에서 실제 표시되는 텍스트와 수식 문맥의 텍스트만 수집한다."""

    _ignored_tags = {"head", "script", "style", "template", "noscript"}
    _formula_tags = {"pre", "math"}
    _block_tags = {
        "address", "article", "aside", "blockquote", "body", "caption", "dd", "div",
        "dl", "dt", "fieldset", "figcaption", "figure", "footer", "form", "h1", "h2",
        "h3", "h4", "h5", "h6", "header", "hr", "html", "legend", "li", "main", "nav",
        "ol", "p", "pre", "section", "table", "tbody", "td", "tfoot", "th", "thead",
        "tr", "ul",
    }
    _void_tags = {
        "area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
        "param", "source", "track", "wbr",
    }
    _formula_markers = re.compile(r"(?:^|[-_])(formula|equation|math|latex)(?:$|[-_])", re.I)

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self._stack = []
        self.visible = []
        self.formula = []

    def handle_starttag(self, tag, attrs):
        attrs = {key: value or "" for key, value in attrs}
        classes = attrs.get("class", "").split()
        style = re.sub(r"\s+", "", attrs.get("style", "").lower())
        ignored = (
            tag in self._ignored_tags
            or "hidden" in attrs
            or "display:none" in style
            or "visibility:hidden" in style
        )
        formula = (
            tag in self._formula_tags
            or attrs.get("role", "").lower() == "math"
            or any(self._formula_markers.search(value) for value in classes)
        )
        parent_ignored = any(in_ignored for _, in_ignored, _ in self._stack)
        parent_formula = any(in_formula for _, _, in_formula in self._stack)
        if not parent_ignored and (tag == "br" or tag in self._block_tags):
            self.visible.append("\n")
            if parent_formula:
                self.formula.append("\n")
        if formula and not parent_formula and not parent_ignored and not ignored:
            self.formula.append("\n")
        if tag in self._void_tags:
            return
        self._stack.append((tag, ignored, formula))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self._void_tags:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for index in range(len(self._stack) - 1, -1, -1):
            if self._stack[index][0] == tag:
                if tag in self._block_tags and not any(
                    ignored for _, ignored, _ in self._stack
                ):
                    self.visible.append("\n")
                    if any(formula for _, _, formula in self._stack):
                        self.formula.append("\n")
                del self._stack[index:]
                break

    def handle_data(self, data):
        if any(ignored for _, ignored, _ in self._stack):
            return
        self.visible.append(data)
        if any(formula for _, _, formula in self._stack):
            self.formula.append(data)


def _visible_html_text(raw):
    parser = _VisibleHTMLText()
    parser.feed(raw)
    parser.close()
    return "".join(parser.visible), "".join(parser.formula)


def _formula_remnant_hits(formula_text):
    """이미 수식 문맥으로 한정된 텍스트에서 접근성/LaTeXML 잔재를 반환한다."""
    return [label for label, pattern in FORMULA_SPEECH_REMNANTS if pattern.search(formula_text)]


def _machine_translation_residue_hits(text):
    """의미 왜곡 가능성이 높고 대체 표현이 명확한 직역 잔재를 반환한다."""
    return [label for label, pattern in MACHINE_TRANSLATION_RESIDUE if pattern.search(text)]


def _pdf_formula_remnant_hits(formula_text):
    """PDF에서는 전용 변환 토큰 또는 한 줄 안에서 반복된 낭독 표지만 실패로 본다."""
    hits = []
    lines = formula_text.splitlines() or [formula_text]
    for label, pattern in FORMULA_SPEECH_REMNANTS:
        if label in PDF_STRONG_REMNANT_LABELS:
            found = pattern.search(formula_text) is not None
        else:
            found = any(len(pattern.findall(line)) >= 2 for line in lines)
        if found:
            hits.append(label)
    return hits


def _pdf_formula_text(text):
    """PDF에서는 수식 신호 행과 줄바꿈으로 감긴 이웃 행을 함께 고른다."""
    lines = text.splitlines()
    selected = set()
    for index, line in enumerate(lines):
        if not FORMULA_CONTEXT_SIGNAL.search(line):
            continue
        selected.add(index)
        for neighbor in (index - 1, index + 1):
            if not (0 <= neighbor < len(lines)):
                continue
            wrapped = lines[neighbor].strip()
            if (
                wrapped
                and _pdf_formula_remnant_hits(wrapped)
                and len(wrapped) <= 80
                and not re.search(r"[.!?。]\s*$", wrapped)
            ):
                selected.add(neighbor)
    return "\n".join(lines[index] for index in sorted(selected))


# ---- 최종 PDF 검사 (모드 A/B 공통) --------------------------------------
def check_final_pdf(rep, final_pdf, orig_pdf):
    final_pages = _pdf_page_count(final_pdf)
    orig_pages = _pdf_page_count(orig_pdf)
    rep.ok(f"페이지 수: 최종 {final_pages}p / 원본 {orig_pages}p")

    # 페이지 수 비율
    if orig_pages > 0:
        ratio = final_pages / orig_pages
        if ratio < RATIO_FAIL_LOW or ratio > RATIO_FAIL_HIGH:
            rep.fail(
                f"페이지 비율 {ratio:.2f}배 (원본 대비). 정상 범위를 크게 벗어났다. "
                f">2.0이면 원문 페이지를 통째로 캡처·삽입했을 가능성이 높다 — "
                f"figures/fig-*.png만 본문 위치에 삽입하고 pages/page-*.png는 넣지 마라. "
                f"<0.5이면 문단 누락을 의심하라."
            )
        elif ratio < RATIO_WARN_LOW or ratio > RATIO_WARN_HIGH:
            rep.warn(f"페이지 비율 {ratio:.2f}배 — ±30% 밖이다. 누락/레이아웃 점검 권장.")
        else:
            rep.ok(f"페이지 비율 {ratio:.2f}배 — 정상 범위(±30%).")

    # 페이지 통 캡처 검출: 단일 이미지가 페이지를 지배 + 본문 희박
    d = fitz.open(final_pdf)
    hard_hits = []      # frac > IMG_FRAC_HARD
    sparse_hits = []    # frac > IMG_FRAC_SPARSE and 본문 희박
    for i, pg in enumerate(d, start=1):
        pa = pg.rect.width * pg.rect.height
        if pa <= 0:
            continue
        worst = 0.0
        for info in pg.get_image_info():
            bb = info.get("bbox")
            if not bb:
                continue
            r = fitz.Rect(bb)
            frac = (r.width * r.height) / pa
            worst = max(worst, frac)
        if worst > IMG_FRAC_HARD:
            hard_hits.append((i, worst))
        elif worst > IMG_FRAC_SPARSE and len(pg.get_text().strip()) < SPARSE_TEXT_LEN:
            sparse_hits.append((i, worst))
    d.close()

    if hard_hits:
        pv = ", ".join(f"p{p}({f:.0%})" for p, f in hard_hits[:5])
        rep.fail(
            f"단일 이미지가 페이지 면적의 {IMG_FRAC_HARD:.0%} 초과인 페이지 {len(hard_hits)}개 "
            f"[{pv}]. 원문 페이지 통 캡처로 판단된다. pages/page-*.png는 좌표 계산용 "
            f"보조자료다 — figures/fig-*.png를 추출해 본문 위치에 삽입하라."
        )
    if sparse_hits:
        pv = ", ".join(f"p{p}({f:.0%})" for p, f in sparse_hits[:5])
        rep.fail(
            f"본문이 거의 없이 큰 이미지({IMG_FRAC_SPARSE:.0%} 초과)만 있는 페이지 "
            f"{len(sparse_hits)}개 [{pv}]. 캡션만 달린 페이지 통 캡처의 전형이다. "
            f"페이지 단위 이미지 삽입을 제거하고 섹션 구조 기반 2단 본문으로 재구성하라."
        )
    if not hard_hits and not sparse_hits:
        rep.ok("페이지 통 캡처 없음 — 이미지가 본문을 지배하는 페이지가 없다.")

    # 최종 PDF 텍스트의 금지 문자열
    txt = _pdf_text(final_pdf)
    hit = [s for s in FORBIDDEN_STRINGS if s in txt]
    if hit:
        rep.fail(
            f"최종 PDF 텍스트에 금지 문자열 {hit} 발견. "
            f"'원문 p.N' / '레이아웃 보존'은 페이지 통 캡처·덤프의 흔적이다. "
            f"해당 구성을 제거하라."
        )
    else:
        rep.ok("최종 PDF 텍스트: 금지 문자열 없음.")

    translation_hits = _machine_translation_residue_hits(txt)
    if translation_hits:
        rep.fail(
            f"최종 PDF에 고신뢰 기계번역 잔재 {translation_hits} 발견. 원문의 논리 구조와 "
            f"전문 용어를 대조해 자연스러운 학술 한국어로 다시 작성하라."
        )
    else:
        rep.ok("최종 PDF: 고신뢰 기계번역 잔재 없음.")

    formula_hits = _pdf_formula_remnant_hits(_pdf_formula_text(txt))
    if formula_hits:
        rep.fail(
            f"최종 PDF에 수식 변환 잔재 {formula_hits} 발견. screen-reader/LaTeXML이 "
            f"중복 생성한 '아래 첨자', 'superscript', 'textsubscript' 등의 문자열을 "
            f"제거하고, 수식은 monospace ASCII/유니코드 한 벌로만 다시 작성하라."
        )
    else:
        rep.ok("최종 PDF: screen-reader/LaTeXML 수식 변환 잔재 없음.")

    # LaTeX 잔재 + 인라인 인용 잔존 (페이지 단위)
    d = fitz.open(final_pdf)
    latex_pages, cite_pages = [], []
    for i, pg in enumerate(d, start=1):
        ptxt = pg.get_text()
        if LATEX_REMNANT.search(ptxt):
            latex_pages.append(i)
        for m in INLINE_CITE.finditer(ptxt):
            if not CITE_OK_CONTEXT.search(ptxt[max(0, m.start() - 3):m.start()]):
                cite_pages.append(i)
                break
    d.close()

    if latex_pages:
        rep.fail(
            f"LaTeX 잔재 노출: 페이지 {latex_pages}. 백슬래시 명령(\\textrm, \\mathbb, "
            f"\\tag, \\frac 등)이나 '$$'가 최종 산출물에 인쇄됐다 — 규칙 4에 따라 "
            f"수식을 monospace ASCII/유니코드로 손수 변환하라."
        )
    else:
        rep.ok("LaTeX 잔재 없음 — 수식이 변환된 상태다.")

    if cite_pages:
        rep.warn(
            f"인라인 인용 [n] 잔존 의심: 페이지 {cite_pages}. 규칙 7에 따라 본문 인용 "
            f"번호는 제거하고 문장을 다듬어야 한다 ('∈ [0,1]' 같은 수식 구간이면 무시)."
        )
    else:
        rep.ok("인라인 인용 [n] 잔존 없음.")

    # 경어체 검사 (표지 1페이지는 안내문에 경어체가 정상이므로 제외)
    d = fitz.open(final_pdf)
    body_txt = "".join(pg.get_text() for pg in list(d)[1:])
    d.close()
    n_hab = len(re.findall("습니다", body_txt))
    if n_hab > HABNIDA_LIMIT:
        rep.fail(
            f"본문 '습니다' {n_hab}회(> {HABNIDA_LIMIT}) — 경어체/기계번역투다. "
            f"규칙 3에 따라 문어체 평서형('~한다')으로 통일하라."
        )
    else:
        rep.ok(f"문체: 본문 '습니다' {n_hab}회(≤ {HABNIDA_LIMIT}) — 경어체 신호 없음.")


# ---- HTML 검사 (모드 A) --------------------------------------------------
def check_html(rep, html_path, workdir, orig_pdf, manifest):
    with open(html_path, encoding="utf-8") as f:
        raw = f.read()
    visible_text, formula_text = _visible_html_text(raw)

    # 1) 페이지 캡처 참조 금지
    if "pages/page-" in raw:
        rep.fail(
            "HTML이 'pages/page-*'를 참조한다. figures/pages/page-NN.png는 좌표 "
            "계산용 보조자료일 뿐 산출물에 넣지 않는다 — figures/fig-*.png를 삽입하라."
        )
    else:
        rep.ok("HTML: 'pages/page-*' 참조 없음.")

    # 2) 금지 문자열
    hit = [s for s in FORBIDDEN_STRINGS if s in raw]
    if hit:
        rep.fail(
            f"HTML에 금지 문자열 {hit} 발견. '원문 p.N 번역' 식 페이지 단위 덤프나 "
            f"'레이아웃 보존' 캡션은 계약 위반이다. 섹션 구조 기반 2단 본문으로 재구성하라."
        )
    else:
        rep.ok("HTML: 금지 문자열 없음.")

    # 2b) 템플릿 예시/placeholder 잔존 금지
    placeholders = [s for s in PLACEHOLDER_PATTERNS if s in raw]
    if placeholders:
        rep.fail(
            f"HTML에 템플릿 placeholder/예시 문자열 {placeholders[:8]} 발견. "
            f"assets/template.html의 skeleton 값을 실제 논문 메타데이터와 본문으로 교체하라."
        )
    else:
        rep.ok("HTML: 템플릿 placeholder 잔존 없음.")

    # 2c) screen-reader/LaTeXML 수식 중복 낭독 잔재 금지
    formula_hits = _formula_remnant_hits(formula_text)
    if formula_hits:
        rep.fail(
            f"HTML에 수식 변환 잔재 {formula_hits} 발견. 수식의 접근성 텍스트·LaTeX·"
            f"시각 표기가 한 문장에 중복 삽입된 상태다. 잔재를 제거하고 monospace "
            f"ASCII/유니코드 수식 한 벌과 평문 해설만 남겨라."
        )
    else:
        rep.ok("HTML: screen-reader/LaTeXML 수식 변환 잔재 없음.")

    # 2d) 최종 HTML의 실제 표시 텍스트에 원시 LaTeX 문법 금지
    if LATEX_REMNANT.search(visible_text):
        rep.fail(
            "HTML에 LaTeX 잔재 노출 발견. 백슬래시 명령(\\textrm, \\mathbb, "
            "\\tag, \\frac 등)이나 '$$'를 monospace ASCII/유니코드 수식으로 변환하라."
        )
    else:
        rep.ok("HTML: 표시 텍스트에 LaTeX 잔재 없음.")

    # 2e) 반복적으로 관찰된 고신뢰 기계번역 직역 잔재 금지
    translation_hits = _machine_translation_residue_hits(visible_text)
    if translation_hits:
        rep.fail(
            f"HTML에 고신뢰 기계번역 잔재 {translation_hits} 발견. 'out-of-distribution'의 "
            f"배포 의미 오역, 중복 양태, 부자연스러운 영어 어순을 원문과 대조해 교정하라."
        )
    else:
        rep.ok("HTML: 고신뢰 기계번역 잔재 없음.")

    # 3) <img> src 존재/비어있지 않음
    srcs = re.findall(r"<img[^>]*\bsrc\s*=\s*[\"']([^\"']+)[\"']", raw, re.IGNORECASE)
    n_img = len(srcs)
    rel_srcs = [s for s in srcs if not re.match(r"^(https?:)?//|^data:", s, re.IGNORECASE)]
    missing, empty = [], []
    for s in rel_srcs:
        p = os.path.normpath(os.path.join(os.path.dirname(html_path), _html.unescape(s)))
        if not os.path.exists(p):
            missing.append(s)
        elif os.path.getsize(p) == 0:
            empty.append(s)
    if missing:
        rep.fail(f"HTML img 경로 {len(missing)}개가 존재하지 않는다: {missing[:5]}. "
                 f"상대경로와 실제 figures/ 파일명을 맞춰라.")
    if empty:
        rep.fail(f"HTML img {len(empty)}개가 0바이트다: {empty[:5]}. 추출을 다시 하라.")
    if not missing and not empty and rel_srcs:
        rep.ok(f"HTML img {len(rel_srcs)}개: 상대경로 파일 모두 존재하고 비어있지 않다.")

    # 4) 표/수식 재구성
    n_table = len(re.findall(r"<table[\s>]", raw, re.IGNORECASE))
    n_equation = len(re.findall(r"<pre(?:\s|>)", raw, re.IGNORECASE))

    if manifest is not None:
        n_fig_m = len(manifest.get("figures", []))
        n_tab_m = len(manifest.get("tables", []))
        if n_img >= n_fig_m:
            rep.ok(f"그림 개수: HTML img {n_img}개 ≥ manifest figures {n_fig_m}개.")
        else:
            rep.fail(
                f"그림 누락: HTML img {n_img}개 < manifest figures {n_fig_m}개. "
                f"manifest에 적은 그림을 모두 추출·삽입하라."
            )
        if n_table >= n_tab_m:
            rep.ok(f"표 개수: HTML <table> {n_table}개 ≥ manifest tables {n_tab_m}개.")
        else:
            rep.fail(
                f"표 누락/미재구성: HTML <table> {n_table}개 < manifest tables {n_tab_m}개. "
                f"표는 이미지가 아니라 HTML <table>로 재구성하라."
            )
        n_eq_m = manifest.get("display_equations")
        if isinstance(n_eq_m, int):
            if n_equation >= n_eq_m:
                rep.ok(f"수식 개수: HTML <pre> {n_equation}개 ≥ manifest display_equations {n_eq_m}개.")
            else:
                rep.fail(
                    f"수식 누락: HTML <pre> {n_equation}개 < manifest display_equations {n_eq_m}개. "
                    f"디스플레이 수식은 monospace <pre> 블록으로 재구성하라."
                )
        else:
            rep.warn("manifest.display_equations가 정수가 아니다 — 수식 개수 검사를 생략한다.")
    else:
        rep.warn("manifest.json 없음 — 2단계에서 작성 권장. 개수 기반 검사 대신 휴리스틱만 수행한다.")
        if n_img == 0:
            rep.fail(
                "HTML에 <img>가 하나도 없다. 원본 그림을 figures/fig-*.png로 추출해 "
                "본문 위치에 삽입하라 (그림 생략 금지)."
            )
        else:
            rep.ok(f"HTML img {n_img}개 존재.")
        orig_tables = _count_table_refs(_pdf_text(orig_pdf))
        if orig_tables > 0 and n_table == 0:
            rep.fail(
                f"원문에 'Table' 참조가 {orig_tables}회 있으나 HTML <table>가 0개다. "
                f"표를 이미지가 아닌 HTML <table>로 재구성하라."
            )
        elif orig_tables > 0:
            rep.ok(f"표: 원문 Table 참조 {orig_tables}회, HTML <table> {n_table}개 존재.")
        else:
            rep.ok("표: 원문에 Table 참조가 없다 — 표 검사 생략.")

    # 5) 경어체 신호
    n_hab = len(re.findall("습니다", raw))
    if n_hab > HABNIDA_LIMIT:
        rep.fail(
            f"'습니다' {n_hab}회(> {HABNIDA_LIMIT}) — 경어체/기계번역투로 판단된다. "
            f"translation-rules.md의 문어체 평서형('~한다')으로 통일하라."
        )
    else:
        rep.ok(f"문체: '습니다' {n_hab}회(≤ {HABNIDA_LIMIT}) — 경어체 신호 없음.")


# ---- 최종 PDF 자동 탐색 (모드 A) -----------------------------------------
def _find_final_pdf(workdir):
    patterns = ["*_ko_translation_layout.pdf", "*_paper_translate_ko.pdf"]
    cands = []
    for base in (workdir, os.path.dirname(os.path.abspath(workdir.rstrip("/")))):
        for pat in patterns:
            cands.extend(glob.glob(os.path.join(base, pat)))
    # 중복 제거, 존재하는 것만
    seen, out = set(), []
    for c in cands:
        rp = os.path.realpath(c)
        if rp not in seen and os.path.exists(c):
            seen.add(rp)
            out.append(c)
    return out


def mode_workdir(workdir, final_arg):
    rep = Report()
    workdir = workdir.rstrip("/")
    if not os.path.isdir(workdir):
        print(f"[오류] 작업폴더가 디렉토리가 아니다: {workdir}")
        return 2

    orig_pdf = os.path.join(workdir, "original.pdf")
    html_path = os.path.join(workdir, "translation.html")
    figures_dir = os.path.join(workdir, "figures")

    print(f"# 출력 계약 검증 (모드 A) — 작업폴더: {workdir}\n")

    # 필수 입력 존재
    if not os.path.exists(orig_pdf):
        rep.fail(f"original.pdf 없음: {orig_pdf}")
    if not os.path.exists(html_path):
        rep.fail(f"translation.html 없음: {html_path}")
    if not os.path.isdir(figures_dir):
        rep.warn(f"figures/ 디렉토리 없음: {figures_dir}")

    # manifest 로드
    manifest = None
    manifest_path = os.path.join(workdir, "manifest.json")
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, encoding="utf-8") as f:
                manifest = json.load(f)
            rep.ok(f"manifest.json 로드: figures {len(manifest.get('figures', []))}개, "
                   f"tables {len(manifest.get('tables', []))}개, "
                   f"display_equations {manifest.get('display_equations', 'N/A')}.")
        except Exception as e:
            rep.warn(f"manifest.json 파싱 실패({e}) — 휴리스틱 검사로 진행.")

    # HTML 검사
    if os.path.exists(html_path) and os.path.exists(orig_pdf):
        check_html(rep, html_path, workdir, orig_pdf, manifest)
    elif os.path.exists(html_path):
        rep.warn("original.pdf가 없어 표 휴리스틱을 생략한다.")

    # 최종 PDF 결정
    final_pdf = None
    if final_arg:
        if os.path.exists(final_arg):
            final_pdf = final_arg
        else:
            rep.fail(f"--final로 지정한 PDF가 없다: {final_arg}")
    else:
        found = _find_final_pdf(workdir)
        if len(found) == 1:
            final_pdf = found[0]
            rep.ok(f"최종 PDF 자동 탐색: {final_pdf}")
        elif len(found) > 1:
            final_pdf = found[0]
            rep.warn(f"최종 PDF 후보 여러 개 발견 {found} — 첫 번째 사용: {final_pdf}. "
                     f"모호하면 --final로 지정하라.")
        else:
            rep.fail("최종 PDF를 찾지 못했다. --final <최종.pdf>로 지정하라.")

    # 최종 PDF 검사
    if final_pdf and os.path.exists(orig_pdf):
        check_final_pdf(rep, final_pdf, orig_pdf)
    elif final_pdf:
        rep.warn("original.pdf가 없어 페이지 비율 검사를 생략한다.")

    print()
    rep.print()
    return 1 if rep.failed else 0


def mode_pdf_only(final_pdf, orig_pdf):
    rep = Report()
    print(f"# 출력 계약 검증 (모드 B, PDF 소급) — 최종: {final_pdf}\n")
    if not os.path.exists(final_pdf):
        print(f"[오류] 최종 PDF 없음: {final_pdf}")
        return 2
    if not os.path.exists(orig_pdf):
        print(f"[오류] 원본 PDF 없음: {orig_pdf}")
        return 2
    check_final_pdf(rep, final_pdf, orig_pdf)
    print()
    rep.print()
    return 1 if rep.failed else 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1

    if argv[1] == "--pdf-only":
        if len(argv) != 4:
            print("사용법: validate_output.py --pdf-only <최종.pdf> <원본.pdf>")
            return 1
        return mode_pdf_only(argv[2], argv[3])

    # 모드 A: <workdir> [--final <path>]
    workdir = argv[1]
    final_arg = None
    rest = argv[2:]
    i = 0
    while i < len(rest):
        if rest[i] == "--final":
            if i + 1 >= len(rest):
                print("사용법: --final 뒤에 PDF 경로가 필요하다")
                return 1
            final_arg = rest[i + 1]
            i += 2
        else:
            print(f"[경고] 알 수 없는 인자 무시: {rest[i]}")
            i += 1
    return mode_workdir(workdir, final_arg)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
