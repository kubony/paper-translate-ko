---
name: paper-translate-ko
description: arXiv/학술 논문 PDF와 기술 블로그·웹사이트를 원본 레이아웃(2단 학술 스타일, 피겨/표/수식 보존)과 원문 영상 자산을 유지한 한국어 완역 PDF로 변환한다. 사용자가 "논문 번역", "논문을 한글로", "translate paper", "레이아웃 유지 번역", "웹사이트 번역", arXiv ID/PDF/웹 URL을 주며 한국어 버전을 요청할 때, 혹은 논문 요약이 아닌 전문 번역이 필요할 때 반드시 이 스킬을 사용하라.
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
VLA/VLN 논문의 architecture·modality·학습 단계·benchmark를 해석하거나 기존 번역을
전면 교정할 때는 `references/dualvln-translation-lessons-learned.md`도 반드시 읽는다.
이 reference는 source/code/interpretation 분리, temporal input, depth provenance,
benchmark-vs-training 구분, optimizer 문단 경계, multicol 조판 회귀를 실제 실패 사례로 설명한다.
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

논문마다 작업 폴더 하나를 만든다. **폴더명만 보고 어떤 논문인지 알 수 있어야 한다** —
`2410.01273/`처럼 id만 쓰지 말고 제목 slug를 붙인다.

### 폴더명 규칙

```
<식별자>_<Title-Slug>/
```

- `식별자`: arXiv id(`2410.01273`), 학회+id, 또는 웹 출처면 `YYYY-MM-DD_<발행처>`.
- `Title-Slug`: **원문 제목**을 하이픈으로 이은 형태. 영문 제목은 그대로,
  대소문자 유지, 부제는 앞부분만 써도 되며 전체 60자 이내로 줄인다.
  콜론·슬래시·따옴표 등 파일시스템에 위험한 문자는 제거한다.
- 예시:
  - `2410.01273_CANVAS-Commonsense-Aware-Navigation-System/`
  - `2511.20216_CostNav-Navigation-Benchmark-Economic-Cost/`
  - `2026-07-17_Sunday-Robotics_ACT-2-Preview-Generalizing-Reliability/`

여러 산출물을 한 레포에 모을 때는 출처 성격으로 한 단계 분류한다.

```
papers/   # arXiv·학회 논문 PDF 번역
web/      # 기업·연구소 블로그, 챌린지 페이지 등 웹 아티클 1편 번역
sites/    # 웹사이트 전체(여러 route) 아카이브 번역
```

### 폴더 내부

```
<식별자>_<Title-Slug>/
  README.md                            # 서지 정보·원문 링크·산출물·자산 요약
  original.pdf                         # 원본 PDF (웹 출처면 없을 수 있음)
  metadata.json                        # (arXiv일 때) 서지 정보
  manifest.json                        # 2단계에서 작성: 그림/표/수식 목록 (검증 기준)
  figures/                             # 추출한 그림 PNG + pages/ 미리보기
  assets/                              # 원문 미디어 (웹 출처면 필수, 아래 자산 정책 참조)
    videos/<slug>.mp4                  #   수집한 영상·애니메이션 원본
    videos/thumbs/<slug>.jpg           #   ffmpeg 첫 프레임 썸네일
    images/                            #   (--include-images 시) 원문 이미지
    videos.json                        #   자산 매니페스트 (url·local·길이·sha256)
    ASSETS.md                          #   사람이 읽는 자산 목록
  translation.html                     # 번역 HTML (template.html 복사본)
  <식별자>_ko_translation_layout.pdf   # 최종 산출물
```

`README.md`에는 최소한 원문 제목·저자·발표처·원문 URL·번역 생성일·최종 PDF
파일명·자산 개수를 적는다. 폴더만 열어봐도 출처를 추적할 수 있어야 한다.

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
6. **웹 출처는 영상 자산을 반드시 확보하고 본문에 링크한다.** 원문이 웹 페이지면
   재생되는 영상·애니메이션이 논문의 그림에 해당한다. 링크만 남기면 원문이 내려갈 때
   근거가 사라지므로 **레포에 파일로 보관**하고, 번역문의 해당 위치에 썸네일과
   로컬 경로·원본 URL을 함께 넣는다(아래 "미디어 자산 정책").
7. **폴더명에 논문 제목 slug를 포함한다.** id만 있는 폴더명은 계약 위반이다.

## 미디어 자산 정책

원문이 웹 페이지이거나, 논문이라도 영상이 있는 프로젝트 페이지를 가지고 있으면
(`metadata.json`의 링크, 논문 표지의 project page URL) 다음을 수행한다.

1. `scripts/fetch_web_assets.py`로 **영상·애니메이션 GIF를 최대한 수집**한다.
   원문 route가 여럿이면 URL을 모두 인자로 준다.

   ```bash
   python3 scripts/fetch_web_assets.py --out <작업폴더>/assets \
     <page_url> [<page_url> ...] [--include-images]
   ```

   - 먼저 `--dry-run`으로 개수·총용량을 확인한 뒤 본 수집을 돌린다.
   - 헤드리스 Chrome DOM + 정적 HTML을 모두 훑어 `<video>`/`<source>`/`poster`/
     srcset/스크립트 하드코딩 URL을 잡는다. YouTube·Vimeo·m3u8은 yt-dlp에 위임한다.
   - 페이지가 영상에 붙여 둔 원문 제목(Next.js RSC payload의 `{"url":...,"title":...}`,
     `<video title=...>`)이 있으면 `videos.json`의 `title`로 기록된다. **캡션은 이 제목을
     번역해 쓰고**, 없을 때만 `context`를 근거로 직접 작성한다.
   - 이미 내려받은 뒤 제목만 다시 채우려면 `--refresh-titles`를 쓴다(재다운로드 없음).
   - 산출물: `assets/videos/*`, `assets/videos/thumbs/*.jpg`, `assets/videos.json`,
     `assets/ASSETS.md`.
2. 저장소에 커밋할 때 **바이너리는 Git LFS로 추적**한다. 레포 `.gitattributes`에
   `*.mp4 *.webm *.mov *.m4v *.gif` 패턴이 등록되어 있어야 한다.

   **용량이 큰 수집본은 GCS로 미러링한다.** 웹사이트 전체 아카이브는 한 건이
   수 GB가 되어 Git LFS 무료 한도(1 GiB)를 넘긴다. 이때는 오브젝트 스토리지에
   원본을 두고 저장소에는 매니페스트·썸네일·작은 파일만 남긴다.

   ```bash
   python3 scripts/mirror_assets_gcs.py <작업폴더> --bucket <버킷> --prune-over-mib 25
   ```

   업로드된 자산에는 `remote`(gs:// URI)와 `remote_url`(브라우저 링크)이 기록되고,
   `--prune-over-mib`를 넘는 로컬 파일은 삭제된다(썸네일은 항상 남는다).
   번역문에서는 로컬 경로 대신 `remote_url`을 링크하면 되고, 검증기는 둘 중
   하나만 링크되어 있으면 통과시킨다.
3. 번역 HTML의 해당 위치에 **영상 카드**를 넣는다. 그림 캡션과 같은 급으로 다루고,
   썸네일 이미지 + 한국어 캡션 + 로컬 파일 링크 + 원본 URL을 모두 표기한다
   (`assets/example.html`의 `.video-card` 참조).

   ```html
   <figure class="video-card">
     <a href="assets/videos/cut_zucchini_compressed-ab12cd.mp4">
       <img src="assets/videos/thumbs/cut_zucchini_compressed-ab12cd.jpg" alt="">
     </a>
     <figcaption>
       <b>영상 3.</b> 애호박 절단 — 손잡이 재파지 후 절단 재개.
       <span class="video-links">
         ▶ <a href="assets/videos/cut_zucchini_compressed-ab12cd.mp4">레포 사본</a>
         · <a href="https://website.pi-asset.com/pi07/cut_zucchini_compressed.mp4">원본</a>
       </span>
     </figcaption>
   </figure>
   ```

4. 수집했지만 본문에 배치할 자리가 없는 영상은 **문서 말미의 "영상 자산" 부록**에
   표로 모아 남긴다. 수집한 자산이 번역문 어디에서도 참조되지 않는 상태로 두지 않는다.
5. 영상 캡션은 원문 캡션이 있으면 번역하고, 없으면 `videos.json`의 `context`
   (영상 직전 본문 텍스트)를 근거로 한 줄 요약을 직접 작성한다. 추측으로 성능
   수치나 실험 조건을 지어내지 않는다.

## 워크플로우

### 1. 입력 확보

- **arXiv ID/URL**이면: `python3 scripts/fetch_arxiv.py <arxiv_id> <작업폴더>` 로
  `original.pdf`와 `metadata.json`(제목·저자·소속·초록·comment·발표정보)을 받는다.
  버전 접미사나 abs/pdf URL을 그대로 넣어도 id가 정규화된다.
- **로컬 PDF**면 그 파일을 `original.pdf`로 쓴다. 서지 정보는 아래 2단계에서 본문으로 파악한다.
- **웹 아티클/웹사이트**면 원문 URL 목록을 확정한다(사이트 전체면 route를 모두 열거).
  원문 PDF가 없으므로 2단계 파악은 페이지 본문으로 하고, 3-1단계 자산 수집이 필수다.

작업 폴더 이름은 이 시점에 위 "폴더명 규칙"대로 짓는다 — 제목을 확인하기 전이라면
임시로 만들고, 2단계에서 제목을 확인한 직후 `<식별자>_<Title-Slug>`로 이름을 고친다.

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

### 3-1. 웹 미디어 자산 수집 (웹 출처면 필수)

원문이 웹 아티클·웹사이트이거나 영상이 있는 프로젝트 페이지를 가진 논문이면
번역 **전에** 자산을 확보한다. 번역하면서 "여기 영상이 있었다"를 사후에 복원하기는 어렵다.

```bash
# 1) 무엇이 얼마나 있는지 먼저 확인
python3 scripts/fetch_web_assets.py --out <작업폴더>/assets --dry-run <page_url> ...

# 2) 실제 수집 (여러 route는 URL을 나열, 이미지까지 필요하면 --include-images)
python3 scripts/fetch_web_assets.py --out <작업폴더>/assets <page_url> ...
```

수집 후 `assets/videos.json`을 읽고 각 영상이 원문 어느 섹션에 붙어 있었는지
(`context` 필드)를 파악해, 4단계 번역에서 배치 위치를 미리 정한다.
세부 규칙은 위 "미디어 자산 정책"을 따른다.

### 4. 번역

`references/translation-rules.md`를 **읽고 그 규칙대로 전체를 번역**한다. 핵심만 상기하면:

- 혼합 표기: 전문용어는 영문 원형 + 한글 조사("grounding해야"). 모델명·벤치마크명·데이터셋명·지표명·수치·인명은 원문 유지.
- 디스플레이 수식은 monospace 코드블록에 ASCII/유니코드 근사 표기. LaTeX 렌더 금지.
- 표는 이미지가 아니라 **HTML 표로 재구성**(수치·최고성능 bold 그대로).
- 본문 인라인 인용 번호 `[12]`는 제거하고 문장을 다듬는다.
- 참고문헌은 문서 끝에 요약 목록(원문 제목 유지).
- 문어체 평서형("~한다")으로 통일, 경어체 금지. 초록~부록 전 문단 완역(요약·생략 금지).

**실전에서 실제로 발생한 실패 유형 — 재발 금지:**

- **용어집 보호 누락**: 전문용어를 먼저 placeholder로 보호하지 않고 기계번역한 뒤
  사후 교정하면 `out-of-distribution → 배포되지 않음`, `visual domain shift → 시각적
  영역의 영향력 있는 변화`처럼 표면 번역이 남는다. 번역 전에 용어집을 적용하고, 복합문은
  주절·대조·인과·관계절로 분해한 뒤 의미 슬롯을 대조한다.
- **논리 관계 붕괴**: `while/however/but`이 포함된 문장에서 예상·관찰·결론을 한 문장에
  유지하려 하지 않는다. 각 명제를 2~3문장으로 나누고, 무엇이 증가·감소했는지와 비교
  기준을 명시한 뒤 원문을 가린 한국어 독립 검토를 수행한다.
- **분류 대립 소실**: `clean/unclean`, `positive/negative`, `in-distribution/out-of-distribution`
  같은 상반된 label을 각각 번역한 뒤 반드시 서로 다른지 확인한다. 같은 번역어가 양쪽에
  반복되면 의미 모순이므로 validator 실패로 처리한다.
- **LaTeX 문법 노출**: `$$ \textrm{GASI}=\mathbb{E}...\tag{3} $$`가 그대로 인쇄됨.
  수식은 반드시 `GASI = E_{g~G}[ E_{r1,r2~R}[ JSD(p_{g,r1} ‖ p_{g,r2}) ] ]`처럼
  ASCII/유니코드로 손수 변환한다. 최종 HTML에 백슬래시나 `$$`가 남으면 실패다.
- **screen-reader/LaTeXML 수식 중복**: `p_IDM(...)` 뒤에 “아래 첨자”,
  `superscript`, `textsubscript`, `leavevmode` 같은 낭독·변환 문자열과 동일 수식의
  LaTeX 표현이 연달아 붙는 사례가 있다. 중복 문자열을 모두 제거하고 수식 한 벌만
  남긴다. 복잡한 수식에는 `.explain-card`로 각 기호와 조건부 입력의 의미를 설명한다.
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
- 넓은 표의 제목도 같은 full-width context에 둔다. `h3 class="section"`을 쓰면 CSS selector가
  `.doc-title, h2.section, h3.section { column-span: all; }`처럼 H3까지 포함해야 한다.
- 렌더 전에 `python3 scripts/check_multicol_layout.py <작업폴더>/translation.html`을 실행한다.
  `h3.section`·`table.wide`·`figure.fig-wide`의 span rule이 빠지면 수정 전까지 렌더하지 않는다.
- wide element가 있는 모든 page는 120–150 dpi로 확대 QA하고, 압축 delivery PDF에서도 반복한다.
- 티저 그림(Figure 1)은 전체 폭 그림 + 캡션 전문 번역 블록으로 넣는다.
- 수집한 영상은 `.video-card`로 본문 해당 위치에 넣고, 배치할 자리가 없는 영상은
  말미 "영상 자산" 부록 표에 모은다. 썸네일·로컬 경로·원본 URL을 모두 남긴다.
  마지막에 `assets/videos.json`의 항목 수와 본문 링크 수를 대조해 누락을 확인한다.

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
`원문 p.`/`레이아웃 보존`, 그림·표·수식 개수(manifest 기준), LaTeX 및
screen-reader/LaTeXML 수식 변환 잔재, 경어체 신호.)

그다음 생성된 PDF를 `Read`로 **처음부터 끝까지** 보고 사람 눈으로 점검한다:

- (a) 표지와 번역 메모가 존재하는가
- (b) 모든 섹션이 완역되었고 누락된 문단이 없는가
- (c) 모든 그림이 삽입되었고 깨지지 않았는가(경로 오류·빈 이미지 없음)
- (d) 표의 수치가 원본과 일치하고 최고성능 bold가 재현되었는가
- (e) 2단 레이아웃이 유지되는가
- (f) 텍스트 오버플로·빈 페이지·잘린 줄이 없는가

문제를 발견하면 `translation.html`을 수정하고 6→7단계를 **반복**한다.
사용자 보고에는 검증 리포트의 종합 판정(PASS/경고 수)을 요약해 포함한다.

### 8. 채팅·Discord 전달용 분할

최종 PDF가 채팅 플랫폼의 첨부 한도를 넘거나 사용자가 분할 전달을 요청하면, 원본
산출물은 그대로 보존하고 **페이지 경계 기준 PDF 조각**을 추가로 만든다. ZIP으로 묶거나
화질을 낮춘 이미지 PDF로 바꾸지 않는다. Discord에서는 한도 변동과 업로드 overhead를
고려해 기본 8 MiB 이하를 사용한다.

```bash
uv run --quiet --with pymupdf python3 scripts/split_pdf_for_delivery.py \
  <최종pdf> <작업폴더>/discord_parts --max-mib 8
```

각 파일명에는 part 번호와 페이지 범위가 포함된다. 생성 후 모든 part가 제한보다 작은지,
페이지 범위가 1페이지부터 마지막 페이지까지 중복·누락 없이 이어지는지 확인하고, part를
순서대로 모두 첨부한다. 분할본은 전달 편의를 위한 사본이며 검증 완료된 전체 PDF를
대체하지 않는다.

## 재사용 lesson learned

- VLA/VLN architecture·modality·temporal context·training/evaluation 분리와 Chrome multicol 회귀 사례:
  `references/dualvln-translation-lessons-learned.md`
- Static multicol preflight:
  `python3 scripts/check_multicol_layout.py <작업폴더>/translation.html`

## 산출물

최종 PDF `<paper_id>_ko_translation_layout.pdf`가 작업 폴더에 있고, 위 검증을
통과했으면 완료다. 사용자에게 산출 경로와 페이지 수를 보고한다.
