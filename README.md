# paper-translate-ko

> arXiv/학술 논문 PDF를 원본 정보 구조에 맞춰 **한국어 완역 PDF**로 재구성하는 Claude Code/Hermes skill.

원본 논문의 섹션 구조를 보존하고, 표지 + 번역 메모, 2단 학술 레이아웃, 원본에서 추출한 피겨 재삽입, HTML로 재구성한 표, monospace 근사 수식과 평문 해설, 한국어/영문 혼합 전문용어 표기, 참고문헌 요약을 생성합니다.

## Installation

### Claude Code Plugin

```bash
/plugin install kubony/paper-translate-ko
```

### Manual Installation

```bash
git clone https://github.com/kubony/paper-translate-ko.git
cp -r paper-translate-ko ~/.claude/skills/
```

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) — PyMuPDF 실행 시 `uv run --with pymupdf` 사용
- Google Chrome 또는 Chromium
  - Linux: `google-chrome`, `google-chrome-stable`, `chromium`, `chromium-browser` 자동 탐지
  - macOS: `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` 자동 탐지
  - 직접 지정: `CHROME_BIN=/path/to/chrome`
- 한글 폰트: Noto Sans KR, Apple SD Gothic Neo 등
- (웹 자산 수집 시) `ffmpeg`/`ffprobe` — 썸네일·길이 추출, `yt-dlp` — YouTube/Vimeo/m3u8

## Usage in Claude Code / Hermes

```text
arXiv 2512.00565 논문을 레이아웃 유지해서 한글로 번역해줘
```

```text
~/Downloads/paper.pdf 이 논문을 한국어 전문 번역 PDF로 만들어줘
```

## Workdir contract

각 논문은 하나의 작업 폴더를 사용합니다. **폴더명에 논문 제목 slug가 들어가야 합니다** —
`<식별자>_<Title-Slug>` 형식이며, 식별자만 있는 폴더명은 검증기가 FAIL 처리합니다.

```text
work/<식별자>_<Title-Slug>/            # 예: 2410.01273_CANVAS-Commonsense-Aware-Navigation
  README.md                            # 서지 정보·원문 링크·산출물·자산 요약
  original.pdf                         # 원본 PDF. fetch_arxiv.py도 이 이름으로 저장함
  metadata.json                        # arXiv 메타데이터
  manifest.json                        # 원문 그림/표/디스플레이 수식 개수 검증 기준
  figures/                             # fig-*.png + pages/page-*.png 미리보기
  assets/                              # 웹 출처 미디어 (fetch_web_assets.py 산출물)
    videos/*.mp4, videos/thumbs/*.jpg
    videos.json, ASSETS.md
  translation.html                     # assets/template.html 기반 번역 HTML
  <식별자>_ko_translation_layout.pdf   # 최종 산출물
```

여러 산출물을 한 저장소에 모을 때는 출처 성격으로 분류합니다:
`papers/`(arXiv·학회 논문), `web/`(웹 아티클 1편), `sites/`(웹사이트 전체 아카이브).

## Web media policy

원문이 웹 아티클/웹사이트이거나 영상이 있는 프로젝트 페이지를 가진 논문이면,
**영상을 저장소에 보관하고 번역문에서 링크**해야 합니다. 링크만 남기면 원문이
내려갈 때 근거가 사라지기 때문입니다.

```bash
# 무엇이 얼마나 있는지 먼저 확인
python3 scripts/fetch_web_assets.py --out "$WORK/assets" --dry-run https://example.com/blog/post

# 실제 수집 (route 여러 개 나열 가능, 이미지까지 필요하면 --include-images)
python3 scripts/fetch_web_assets.py --out "$WORK/assets" https://example.com/blog/post
```

- 헤드리스 Chrome DOM + 정적 HTML을 모두 훑어 `<video>`/`<source>`/`poster`/srcset/
  스크립트 하드코딩 URL과 애니메이션 GIF를 수집하고, YouTube·Vimeo·m3u8은 yt-dlp에 위임합니다.
- 영상마다 ffmpeg 썸네일과 ffprobe 길이·해상도, sha256을 `videos.json`에 기록합니다.
- 번역 HTML에는 `.video-card`(썸네일 + 캡션 + 레포 사본 링크 + 원본 URL)로 넣고,
  본문에 자리가 없는 영상은 말미 "영상 자산" 부록 표에 모읍니다.
- 바이너리는 Git LFS로 추적합니다(`.gitattributes`에 `*.mp4 *.webm *.mov *.m4v *.gif`).
- 검증기는 `assets/videos.json`이 있으면 파일 존재와 **본문 링크 여부**를 강제합니다.

`manifest.json` 예시:

```json
{
  "figures": [{"no": "1", "page": 2, "desc": "시스템 개요"}],
  "tables": [{"no": "1", "page": 5, "desc": "정량 비교"}],
  "display_equations": 7
}
```

## End-to-end quickstart

```bash
REPO=$PWD
WORK=work/2512.00565

# 1. arXiv PDF + metadata. PDF는 $WORK/original.pdf 로 저장됩니다.
python3 scripts/fetch_arxiv.py 2512.00565 "$WORK"

# 2. 원문 PDF를 읽고 manifest.json을 작성한 뒤, 그림 후보/페이지 미리보기 추출
uv run --quiet --with pymupdf python3 scripts/extract_figures.py auto \
  "$WORK/original.pdf" "$WORK/figures"

# 3. assets/template.html을 $WORK/translation.html로 복사하고 실제 번역문으로 교체
cp assets/template.html "$WORK/translation.html"
# Claude Code/Hermes가 translation.html을 완성합니다.

# 4. HTML → PDF
python3 scripts/render_pdf.py \
  "$WORK/translation.html" \
  "$WORK/2512.00565_ko_translation_layout.pdf"

# 5. 필수 검증 게이트. PASS가 아니면 translation.html을 수정하고 4→5를 반복합니다.
uv run --quiet --with pymupdf python3 scripts/validate_output.py \
  "$WORK" --final "$WORK/2512.00565_ko_translation_layout.pdf"

# 6. Discord/채팅 첨부 한도를 넘으면 8 MiB 이하 페이지 조각으로 분할
uv run --quiet --with pymupdf python3 scripts/split_pdf_for_delivery.py \
  "$WORK/2512.00565_ko_translation_layout.pdf" "$WORK/discord_parts" --max-mib 8
```

분할본은 `partNN-of-NN_pages-XXX-YYY.pdf` 형식으로 생성되며, 원본 PDF는 변경하지
않습니다. 모든 part를 페이지 순서대로 첨부하면 됩니다.

## Output quality contract

검증기는 다음 실패 유형을 자동으로 잡습니다.

- `figures/pages/page-*.png` 같은 원문 페이지 통캡처를 본문에 삽입
- `원문 p.N 번역` 식 페이지 단위 텍스트 덤프
- 존재하지 않거나 0바이트인 이미지 경로
- manifest 대비 그림/표/디스플레이 수식 누락
- 표를 HTML `<table>`로 재구성하지 않음
- LaTeX 잔재(`\\frac`, `\\mathbb`, `$$` 등)
- 백슬래시가 벗겨진 LaTeX 매크로(`noindent`, `toprule`, `num[round-mode`)와 풀린 `\\ref` label
- 마크다운 표 원문(`|---|---:|`)이 조판되지 않고 그대로 인쇄됨
- 캡션 자리에 원본 파일명·자산 URL(`teaser_v6.png`)이 남음
- 템플릿 자리표시 잔재(`없음(null)`, `제공되지 않음`)
- 캡션·섹션 번호 이중 인쇄(`그림 1. 그림 1:`, `2.1 2.1 태스크 설계`)
- 본문이 참조하는 `표 N`/`그림 N`에 대응 캡션이 없음(주 결과표 누락 등)
- screen-reader/LaTeXML 수식 변환 잔재(`아래 첨자`, `superscript`, `textsubscript` 등)
- 고신뢰 기계번역 잔재(`건강하게 감소`, `예측할 수 있다고 예상할 수`, `제작대를 제작` 등)
- 본문 인라인 인용 번호 `[12]` 잔존 의심
- 경어체/기계번역투 과다
- template placeholder 문자열 잔존
- 작업 폴더명에 논문 제목 slug 없음(식별자만 있는 폴더명)
- 수집한 영상이 번역문 어디에서도 링크되지 않음 / 자산 파일 누락

## Files

```text
SKILL.md                                  # 전체 workflow와 agent 지침
references/translation-rules.md           # 번역 문체/레이아웃 규칙
references/vla-robotics-translation-glossary.md
scripts/fetch_arxiv.py                    # arXiv PDF + metadata 다운로드
scripts/fetch_web_assets.py               # 웹 아티클 영상/이미지 자산 수집
scripts/extract_figures.py                # PDF 그림 후보 추출/수동 crop
scripts/render_pdf.py                     # HTML → PDF 렌더링
scripts/validate_output.py                # 출력 계약 검증 게이트
scripts/split_pdf_for_delivery.py         # Discord/채팅용 크기 제한 PDF 분할
assets/template.html                      # 실제 작업용 skeleton
assets/example.html                       # 구성요소 예시 HTML
```

## Local sanity checks

```bash
python3 -m py_compile scripts/*.py
python3 scripts/fetch_arxiv.py
python3 scripts/fetch_web_assets.py --help
python3 scripts/render_pdf.py
uv run --quiet --with pymupdf python3 scripts/extract_figures.py
uv run --quiet --with pymupdf python3 scripts/validate_output.py
uv run --quiet --with pymupdf python3 scripts/split_pdf_for_delivery.py --help
```

## License

MIT
