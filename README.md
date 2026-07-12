# paper-translate-ko

> arXiv/학술 논문 PDF를 원본 레이아웃(2단 학술 스타일, 피겨/표/수식 보존)을 유지한 **한국어 완역 PDF**로 변환하는 Claude Code 스킬.

원본 논문의 정보 구조를 그대로 유지합니다: 표지 + 번역 메모, 2단 레이아웃, 원본에서 추출한 피겨 재삽입, HTML로 재구성한 표(수치·bold 강조 보존), ASCII 근사 수식 코드블록, 혼합 표기(전문용어 영문 유지 + 한글 조사), 참고문헌 요약.

## Installation

### Claude Code Plugin (Recommended)

```bash
/plugin install kubony/paper-translate-ko
```

### Manual Installation

```bash
git clone https://github.com/kubony/paper-translate-ko.git
cp -r paper-translate-ko ~/.claude/skills/
```

## Usage

Claude Code에서:

```
arXiv 2512.00565 논문을 레이아웃 유지해서 한글로 번역해줘
```

```
~/Downloads/paper.pdf 이 논문을 한국어 전문 번역 PDF로 만들어줘
```

파이프라인: 원본 PDF에서 피겨를 이미지로 추출 → 번역문을 2단 학술 레이아웃 HTML로 작성 → 헤드리스 Chrome print-to-PDF → 자체 검증(섹션 완역·그림·표 대조).

## Requirements

- **macOS** + **Google Chrome** (헤드리스 print-to-PDF 렌더링)
- **uv** — PyMuPDF를 `uv run --with pymupdf`로 실행 (피겨 추출)
- 한글 폰트: Apple SD Gothic Neo (macOS 기본) 또는 Noto Sans KR

## Structure

```
SKILL.md                         # 7단계 워크플로우
references/translation-rules.md  # 번역 스타일 규칙 (참조 번역본에서 도출)
scripts/fetch_arxiv.py           # arXiv PDF + 메타데이터 다운로드
scripts/extract_figures.py       # 피겨 이미지 추출 (auto/crop)
scripts/render_pdf.py            # HTML → PDF 렌더링
assets/template.html             # 2단 학술 레이아웃 HTML 템플릿
```

## License

MIT
