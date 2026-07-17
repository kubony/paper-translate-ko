# paper-translate-ko

> arXiv/학술 논문 PDF를 원본 정보 구조에 맞춰 **한국어 완역 PDF**로 재구성하는 Claude Code/Hermes skill.

원본 논문의 섹션 구조를 보존하고, 표지 + 번역 메모, 2단 학술 레이아웃, 원본에서 추출한 피겨 재삽입, HTML로 재구성한 표, monospace 근사 수식, 한국어/영문 혼합 전문용어 표기, 참고문헌 요약을 생성합니다.

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

## Usage in Claude Code / Hermes

```text
arXiv 2512.00565 논문을 레이아웃 유지해서 한글로 번역해줘
```

```text
~/Downloads/paper.pdf 이 논문을 한국어 전문 번역 PDF로 만들어줘
```

## Workdir contract

각 논문은 하나의 작업 폴더를 사용합니다.

```text
work/<paper_id>/
  original.pdf                         # 원본 PDF. fetch_arxiv.py도 이 이름으로 저장함
  metadata.json                        # arXiv 메타데이터
  manifest.json                        # 원문 그림/표/디스플레이 수식 개수 검증 기준
  figures/                             # fig-*.png + pages/page-*.png 미리보기
  translation.html                     # assets/template.html 기반 번역 HTML
  <paper_id>_ko_translation_layout.pdf # 최종 산출물
```

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
```

## Output quality contract

검증기는 다음 실패 유형을 자동으로 잡습니다.

- `figures/pages/page-*.png` 같은 원문 페이지 통캡처를 본문에 삽입
- `원문 p.N 번역` 식 페이지 단위 텍스트 덤프
- 존재하지 않거나 0바이트인 이미지 경로
- manifest 대비 그림/표/디스플레이 수식 누락
- 표를 HTML `<table>`로 재구성하지 않음
- LaTeX 잔재(`\\frac`, `\\mathbb`, `$$` 등)
- 본문 인라인 인용 번호 `[12]` 잔존 의심
- 경어체/기계번역투 과다
- template placeholder 문자열 잔존

## Files

```text
SKILL.md                                  # 전체 workflow와 agent 지침
references/translation-rules.md           # 번역 문체/레이아웃 규칙
references/vla-robotics-translation-glossary.md
scripts/fetch_arxiv.py                    # arXiv PDF + metadata 다운로드
scripts/extract_figures.py                # PDF 그림 후보 추출/수동 crop
scripts/render_pdf.py                     # HTML → PDF 렌더링
scripts/validate_output.py                # 출력 계약 검증 게이트
assets/template.html                      # 실제 작업용 skeleton
assets/example.html                       # 구성요소 예시 HTML
```

## Local sanity checks

```bash
python3 -m py_compile scripts/*.py
python3 scripts/fetch_arxiv.py
python3 scripts/render_pdf.py
uv run --quiet --with pymupdf python3 scripts/extract_figures.py
uv run --quiet --with pymupdf python3 scripts/validate_output.py
```

## License

MIT
