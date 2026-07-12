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
  figures/                             # 추출한 그림 PNG + pages/ 미리보기
  translation.html                     # 번역 HTML (template.html 복사본)
  <paper_id>_ko_translation_layout.pdf # 최종 산출물
```

## 워크플로우

### 1. 입력 확보

- **arXiv ID/URL**이면: `python3 scripts/fetch_arxiv.py <arxiv_id> <작업폴더>` 로
  PDF와 `metadata.json`(제목·저자·소속·초록·comment·발표정보)을 받는다.
  버전 접미사나 abs/pdf URL을 그대로 넣어도 id가 정규화된다.
- **로컬 PDF**면 그 파일을 `original.pdf`로 쓴다. 서지 정보는 아래 2단계에서 본문으로 파악한다.

### 2. 원문 파악

`Read` 도구로 **PDF 전체를 읽는다**(길면 페이지 범위를 나눠서). 번역 전에
다음을 먼저 정리하라. 구조를 모른 채 번역하면 섹션 누락·오역이 생긴다.

- 섹션 구조(번호·제목 계층)
- 그림 목록(번호·페이지·티저 여부)과 표 목록(번호·페이지)
- 디스플레이 수식 목록과 본문에서 참조되는 식 번호

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

### 5. HTML 작성

`assets/template.html`을 작업 폴더로 복사해 `translation.html`로 쓰고 내용만 교체한다.
템플릿에는 각 컴포넌트(표지·번역 메모·초록·H2 섹션·코드블록 수식·그림+캡션·표·참고문헌)의
사용 예시와 `<!-- 여기서부터 실제 내용으로 교체 -->` 안내 주석이 들어 있다.

- 표지 값(제목/저자/학회/arXiv/생성일)을 채운다. 생성일은 오늘 날짜.
- 이미지 경로는 **상대경로**(`figures/fig-p01-01.png`)로 쓴다.
- 넓은 표/그림은 `class="wide"` / `class="fig-wide"`로 단 전체 폭을 쓴다.
- 티저 그림(Figure 1)은 전체 폭 그림 + 캡션 전문 번역 블록으로 넣는다.

### 6. 렌더링

`python3 scripts/render_pdf.py <작업폴더>/translation.html <작업폴더>/<paper_id>_ko_translation_layout.pdf`

스크립트가 헤드리스 Chrome을 띄워 파일이 안정될 때까지 폴링한 뒤 종료하고,
페이지 수를 보고한다.

### 7. 자체 검증 (필수)

생성된 PDF를 `Read`로 **처음부터 끝까지** 보고 다음을 점검한다:

- (a) 표지와 번역 메모가 존재하는가
- (b) 모든 섹션이 완역되었고 누락된 문단이 없는가
- (c) 모든 그림이 삽입되었고 깨지지 않았는가(경로 오류·빈 이미지 없음)
- (d) 표의 수치가 원본과 일치하고 최고성능 bold가 재현되었는가
- (e) 2단 레이아웃이 유지되는가
- (f) 텍스트 오버플로·빈 페이지·잘린 줄이 없는가

문제를 발견하면 `translation.html`을 수정하고 6→7단계를 **반복**한다.
페이지 수가 원본과 크게 다르면(±30% 초과) 누락이나 레이아웃 문제를 의심하라.

## 산출물

최종 PDF `<paper_id>_ko_translation_layout.pdf`가 작업 폴더에 있고, 위 검증을
통과했으면 완료다. 사용자에게 산출 경로와 페이지 수를 보고한다.
