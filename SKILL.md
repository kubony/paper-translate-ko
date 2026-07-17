---
name: paper-translate-ko
description: arXiv/학술 논문 PDF를 원본 레이아웃(2단 학술 스타일, 피겨/표/수식 보존)을 유지한 한국어 완역 PDF로 변환한다. 사용자가 "논문 번역", "논문을 한글로", "translate paper", "레이아웃 유지 번역", arXiv ID/PDF를 주며 한국어 버전을 요청할 때, 혹은 논문 요약이 아닌 전문 번역이 필요할 때 반드시 이 스킬을 사용하라.
---

# 논문 한국어 전문 번역 (레이아웃 보존)

논문을 **요약하지 말고 완역**한다. 산출물은 원본과 유사한 2단 학술 레이아웃의
한국어 PDF다. 파이프라인은 "원본 PDF에서 피겨를 이미지로 추출 → 번역문을 HTML로
작성 → 헤드리스 Chrome print-to-PDF"이다. LaTeX 렌더링 같은 무거운 의존성은 쓰지 않는다.

번역 스타일의 **모든 세부 규칙은 `references/translation-rules.md`에 있다.
번역을 시작하기 전에 반드시 그 파일을 읽어라.** 이 문서는 규칙을 반복하지 않고
워크플로우와 "왜"를 설명한다.

AI/robotics/VLA/VLN/physical AI 논문과 기술 블로그는 추가로
`references/vla-robotics-translation-glossary.md`를 읽고 그 용어집을 우선 적용한다.
특히 `frontier model`은 **프론티어 모델**이며 절대 “개척 모델”로 번역하지 않는다.
`VLA`, `foundation model`, `policy`, `action`, `pixel goal`, `latent goal`, `embodiment`,
`cross-embodiment`, `dexterous manipulation` 등은 과번역하지 말고 혼합 표기를 유지한다.

## 도구 실행 규약

- Python 스크립트 중 `extract_figures.py`는 pymupdf가 필요하다. 시스템 pip는
  PEP 668로 막혀 있으므로 **반드시 uv로 실행**한다:
  `uv run --quiet --with pymupdf python3 <스크립트> ...`
- `fetch_arxiv.py`와 `render_pdf.py`는 표준 라이브러리만 쓰므로 `python3 ...`로 바로 실행한다.
- 스크립트는 스킬 디렉토리의 `scripts/` 아래에 있다. 절대경로로 호출하라.

## 작업 디렉토리 구조

논문마다 작업 폴더 하나를 만든다(예: `<paper_id>/`):

```
<paper_id>/
  original.pdf                         # 원본 PDF
  metadata.json                        # (arXiv일 때) 서지 정보
  manifest.json                        # 2단계에서 작성: 그림/표/수식 목록 (검증 기준)
  figures/                             # 추출한 그림 PNG + pages/ 미리보기
  translation.html                     # 번역 HTML (template.html 복사본)
  <paper_id>_ko_translation_layout.pdf # 최종 산출물
```

## 출력 계약 (위반 시 산출물 폐기·재작업)

과거 실행에서 규칙을 무시한 열화 산출물(원본 페이지 통 캡처 나열, 페이지 단위
텍스트 덤프, 경어체)이 나왔다. 아래는 **절대 계약**이며, 7단계의 `validate_output.py`가
기계적으로 강제한다.

1. **원문 페이지 통 캡처 이미지 삽입 금지.** `figures/pages/page-NN.png`는 그림
   좌표를 계산하기 위한 **보조자료일 뿐**, 산출물(HTML/PDF)에 절대 넣지 않는다.
2. **"원문 p.N 번역" 식 페이지 단위 텍스트 덤프 금지.** 산출물은 원문 페이지가
   아니라 **섹션 구조에 기반한 2단 레이아웃**이어야 한다.
3. **표를 이미지로 삽입 금지.** 표는 HTML `<table>`로 재구성한다(translation-rules.md 6장).
4. **경어체·기계번역투 금지.** 문어체 평서형("~한다")으로 통일한다(translation-rules.md 3장).
5. **요약·문단 생략 금지.** 초록~부록 전 문단을 완역한다(참고문헌만 요약 허용).

## 워크플로우

### 1. 입력 확보

- **arXiv ID/URL**이면: `python3 scripts/fetch_arxiv.py <arxiv_id> <작업폴더>` 로
  `original.pdf`와 `metadata.json`(제목·저자·소속·초록·comment·발표정보)을 받는다.
  버전 접미사나 abs/pdf URL을 그대로 넣어도 id가 정규화된다.
- **로컬 PDF**면 그 파일을 `original.pdf`로 쓴다. 서지 정보는 아래 2단계에서 본문으로 파악한다.

### 2. 원문 파악

`Read` 도구로 **PDF 전체를 읽는다**(길면 페이지 범위를 나눠서). 번역 전에
다음을 먼저 정리하라. 구조를 모른 채 번역하면 섹션 누락·오역이 생긴다.

- 섹션 구조(번호·제목 계층)
- 그림 목록(번호·페이지·티저 여부)과 표 목록(번호·페이지)
- 디스플레이 수식 목록과 본문에서 참조되는 식 번호

정리한 목록을 작업폴더의 `manifest.json`으로 **반드시 저장**한다(7단계 검증의
기준값이 된다). 스키마:

```json
{
  "figures": [{"no": "1", "page": 2, "desc": "시스템 개요"}],
  "tables":  [{"no": "1", "page": 5, "desc": "정량 비교"}],
  "display_equations": 7
}
```

`no`는 원문 번호, `page`는 원본 PDF 페이지(1-based), `desc`는 한 줄 설명이다.
manifest가 없으면 검증은 휴리스틱으로만 돌고 경고를 낸다.

### 3. 피겨 추출

그림은 다시 그리지 않고 **원본에서 이미지로 추출**해 재삽입한다.

1. `uv run --quiet --with pymupdf python3 scripts/extract_figures.py auto <original.pdf> <작업폴더>/figures`
   실행. `figures/fig-pNN-KK.png`(그림 후보)와 `figures/pages/page-NN.png`(페이지 미리보기)가 생긴다.
2. 생성된 `fig-*.png`를 `Read`로 하나씩 확인한다.
3. 잘못 잘렸거나 빠진 그림이 있으면, 해당 `pages/page-NN.png`(zoom 2, 즉 **픽셀÷2 = PDF 포인트**)를
   `Read`로 보고 좌표를 계산해 수동 크롭한다:
   `uv run --quiet --with pymupdf python3 scripts/extract_figures.py crop <original.pdf> <page> <x0> <y0> <x1> <y1> <out.png>`
4. 본문에 필요한 **모든 그림이 깨끗하게 확보될 때까지 반복**한다.
   auto는 텍스트-only 영역을 그림으로 오인하거나 일부 벡터 그림을 놓칠 수 있다 — crop이 보완책이다.

### 4. 번역

`references/translation-rules.md`를 **읽고 그 규칙대로 전체를 번역**한다. 핵심만 상기하면:

- 혼합 표기: 전문용어는 영문 원형 + 한글 조사("grounding해야"). 모델명·벤치마크명·데이터셋명·지표명·수치·인명은 원문 유지.
- 디스플레이 수식은 monospace 코드블록에 ASCII/유니코드 근사 표기. LaTeX 렌더 금지.
- 표는 이미지가 아니라 **HTML 표로 재구성**(수치·최고성능 bold 그대로).
- 본문 인라인 인용 번호 `[12]`는 제거하고 문장을 다듬는다.
- 참고문헌은 문서 끝에 요약 목록(원문 제목 유지).
- 문어체 평서형("~한다")으로 통일, 경어체 금지. 초록~부록 전 문단 완역(요약·생략 금지).

**실전에서 실제로 발생한 실패 유형 — 재발 금지:**

- **LaTeX 문법 노출**: `$$ \textrm{GASI}=\mathbb{E}...\tag{3} $$`가 그대로 인쇄됨.
  수식은 반드시 `GASI = E_{g~G}[ E_{r1,r2~R}[ JSD(p_{g,r1} ‖ p_{g,r2}) ] ]`처럼
  ASCII/유니코드로 손수 변환한다. 최종 HTML에 백슬래시나 `$$`가 남으면 실패다.
- **코드 토큰 기계 오역**: "CoT"→"간이 침대", "Let G"→"허락하다 G", 표 헤더 "SI"→"(시)".
  약어·기호·표 헤더는 번역 대상이 아니다 — 산문만 번역한다.
- **미번역 잔존**: 원문 영어 문단이 통째로 남음. 완역이 원칙이다.
- **raw 텍스트 추출을 번역 원문으로 사용**: `get_text()` 덤프는 2단 원문의 컬럼 순서를
  뒤섞고("verbal com-arXiv:2410.01273v3 맨드"), 줄바꿈 하이픈("de-\ntection")을 못 잇고,
  사이드바 워터마크까지 흡수한다. **번역 원문은 반드시 Read 도구로 PDF를 시각적으로
  읽어 파악**하고, 문장은 사람이 읽는 순서로 재구성해 번역한다.
- **혼합 캡션**: "Table 1 and Figure 2: ..."를 "표 1 및 그림 2: ..." 하나로 뭉치지 말고,
  표와 그림 **각각의 캡션으로 분리**해 단다.

번역을 서브에이전트에 위임하는 경우, 브리프에 `translation-rules.md`의 문체 규칙과
위 **출력 계약**(경어체 금지·완역·표는 HTML로)을 반드시 포함하라. 다만 **HTML 조립과
7단계 검증은 메인 세션이 직접 수행**한다 — 서브에이전트에는 번역문 텍스트만 받고,
그림 삽입·표 재구성·검증 게이트 통과 책임은 메인 세션이 진다.

### 5. HTML 작성

`assets/template.html`을 작업 폴더로 복사해 `translation.html`로 쓰고 placeholder를 실제 값으로 교체한다.
구성요소 예시는 `assets/example.html`에 있다. `template.html`의 skeleton 값을 남기면
7단계 validator가 placeholder 잔존으로 FAIL 처리한다.

- 표지 값(제목/저자/학회/arXiv/생성일)을 채운다. 생성일은 오늘 날짜.
- 이미지 경로는 **상대경로**(`figures/fig-p01-01.png`)로 쓴다.
- 넓은 표/그림은 `class="wide"` / `class="fig-wide"`로 단 전체 폭을 쓴다.
- 티저 그림(Figure 1)은 전체 폭 그림 + 캡션 전문 번역 블록으로 넣는다.

### 6. 렌더링

`python3 scripts/render_pdf.py <작업폴더>/translation.html <작업폴더>/<paper_id>_ko_translation_layout.pdf`

스크립트가 헤드리스 Chrome을 띄워 파일이 안정될 때까지 폴링한 뒤 종료하고,
페이지 수를 보고한다.

### 7. 자체 검증 (필수 게이트)

먼저 **기계 검증을 통과**해야 한다. 출력 계약 위반을 자동 검출한다:

```
uv run --quiet --with pymupdf python3 scripts/validate_output.py <작업폴더> --final <최종pdf>
```

exit 0(PASS)이어야 완료다. FAIL이면 리포트의 교정 안내대로 `translation.html`을
고치고 6→7단계를 **반복**한다. (검사 항목: 페이지 통 캡처, 페이지 비율, 금지 문자열
`원문 p.`/`레이아웃 보존`, 그림·표 개수(manifest 기준), 경어체 신호.)

그다음 생성된 PDF를 `Read`로 **처음부터 끝까지** 보고 사람 눈으로 점검한다:

- (a) 표지와 번역 메모가 존재하는가
- (b) 모든 섹션이 완역되었고 누락된 문단이 없는가
- (c) 모든 그림이 삽입되었고 깨지지 않았는가(경로 오류·빈 이미지 없음)
- (d) 표의 수치가 원본과 일치하고 최고성능 bold가 재현되었는가
- (e) 2단 레이아웃이 유지되는가
- (f) 텍스트 오버플로·빈 페이지·잘린 줄이 없는가

문제를 발견하면 `translation.html`을 수정하고 6→7단계를 **반복**한다.
사용자 보고에는 검증 리포트의 종합 판정(PASS/경고 수)을 요약해 포함한다.

## 산출물

최종 PDF `<paper_id>_ko_translation_layout.pdf`가 작업 폴더에 있고, 위 검증을
통과했으면 완료다. 사용자에게 산출 경로와 페이지 수를 보고한다.
