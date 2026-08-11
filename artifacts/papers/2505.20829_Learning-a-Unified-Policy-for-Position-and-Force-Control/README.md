# arXiv 2505.20829 한국어 전문 번역

**Learning a Unified Policy for Position and Force Control in Legged Loco-Manipulation**의 초록부터 부록 E·참고문헌까지 전체를 한국어로 옮긴 재현 가능한 번역 artifact다. 원문 figure/table/equation 번호와 본문 인용을 보존했고, 공식 프로젝트 페이지의 보충 영상 14개를 source-native 자산으로 함께 아카이브했다.

- arXiv: <https://arxiv.org/abs/2505.20829>
- 프로젝트: <https://unified-force.github.io/>
- 원문 버전: arXiv `2505.20829v2` (공개 2025-05-27, 수정 2025-10-04)
- 번역 생성일: 2026-08-11

## 주요 산출물

- `translation.pdf`: 최종 A4 19페이지 한국어 전문 번역 PDF
- `translation.html`: 접근 가능한 1쪽 표지 + 2단 한국어 학술 레이아웃
- `original.pdf`: 원문 PDF
- `source/`: arXiv LaTeX source와 참고문헌 원본
- `translations/part*.md`: source line 범위별 한국어 번역 fragment
- `figures/`: 원문 9개 figure 및 프로젝트 영상 preview
- `assets/videos/`: 공식 프로젝트 영상 14개의 로컬 cache (`.gitignore` 대상); 원본 URL·SHA-256·thumbnail은 `assets/videos.json`과 `ASSETS.md`로 재현 가능
- `manifest.json`: canonical entity, asset provenance, self-check 결과
- `citation_map.json`: `main.bbl` 순서의 50개 인용 매핑
- `qa_translation_pages.jpg`: 최종 19페이지 contact-sheet 시각 QA 증거
- `qa_page_stats.json`: 페이지별 white/ink 비율 검사 결과
- `build_translation.py`: fragment와 source-native 자산을 조립하는 재생성 스크립트

## 재생성

```bash
cd artifacts/papers/2505.20829_Learning-a-Unified-Policy-for-Position-and-Force-Control
python3 build_translation.py
python3 ../../../scripts/render_pdf.py translation.html translation.pdf
```

## 검증

```bash
cd /path/to/paper-translate-ko
python3 scripts/check_multicol_layout.py \
  artifacts/papers/2505.20829_Learning-a-Unified-Policy-for-Position-and-Force-Control/translation.html
python3 scripts/validate_cross_references.py \
  artifacts/papers/2505.20829_Learning-a-Unified-Policy-for-Position-and-Force-Control/source/main.tex \
  artifacts/papers/2505.20829_Learning-a-Unified-Policy-for-Position-and-Force-Control/translation.html
uv run --quiet --with pymupdf python3 scripts/validate_output.py \
  artifacts/papers/2505.20829_Learning-a-Unified-Policy-for-Position-and-Force-Control \
  --final artifacts/papers/2505.20829_Learning-a-Unified-Policy-for-Position-and-Force-Control/translation.pdf
```

최종 검증 결과:

- 출력 계약 validator: **PASS**
- figure 교차참조(label → 번호 → href → 참조 횟수): **PASS**
- 2단 wide-element 정적 preflight: **PASS**
- 전 페이지 contact-sheet 시각 QA: **PASS**
- 최종/원문 페이지 수: **19 / 18** (1.06배)
- 빈 페이지, 잘림, 겹침, 표·수식 overflow, 깨진 그림: **없음**

## 보존된 구조

- 그림: 9개 — 1–5, A.6–A.9 (원문은 부록에서 figure counter를 reset하지 않음)
- 표: 3개 — A.1–A.3
- 표시 수식: 9개 — 1–5, A.1–A.4
- 참고문헌: 50개
- 본문 인용 링크: 69개
- 보충 영상: 14개, 모두 본문 부록에서 연결

## 최종 체크섬

```text
translation.html  sha256 3e31a83f2b476e6c8524643a90e537ce1fba3e600f246fcdb033898d31e7eeb0
translation.pdf   sha256 cf174b0abefdbd7dd6f0932420bebf6227af4b2e145f89880b5a4ca0dfd5dd7e
manifest.json     sha256 1587aa3dcac14c192c4bbab4dab069256bdbf9644ffcdee57b99948570c7c6a0
citation_map.json sha256 7400cbcba39c455a9128bccd94c6f8db7faeff02f258cec4d5b33cf0a4503dc0
```
