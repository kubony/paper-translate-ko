# Data-Efficient Excavation Force Estimation for Wheel Loaders — 한국어 전문 번역

- **IEEE 문서 번호:** [11205828](https://ieeexplore.ieee.org/document/11205828)
- **DOI:** [10.1109/ACCESS.2025.3622535](https://doi.org/10.1109/ACCESS.2025.3622535)
- **저널:** IEEE Access, vol. 13, pp. 181846–181862, 2025
- **공개 원문:** [arXiv:2506.22579v2](https://arxiv.org/abs/2506.22579v2)
- **저자:** Armin Abdolmohammadi, Navid Mojahed, Shima Nazari, Bahram Ravani

## 산출물

- [`2506.22579_ko_translation_layout.pdf`](2506.22579_ko_translation_layout.pdf) — 최종 A4 2단 한국어 완역 PDF
- [`translation.html`](translation.html) — 편집 가능한 2단 HTML 원본
- [`original.pdf`](original.pdf) — 번역 기준 공개 원문(arXiv v2)
- [`manifest.json`](manifest.json) — 그림·표·수식 inventory
- [`validation.txt`](validation.txt) — 최종 자동 검증 로그
- [`build_translation.py`](build_translation.py) — 번역 fragment를 최종 HTML로 조립하는 재현 스크립트
- [`render_equations.py`](render_equations.py) — 식 (1)–(28)을 LaTeX에서 벡터 SVG로 재현하는 스크립트
- [`extract_clean_figures.py`](extract_clean_figures.py) — 원문 PDF에서 그림 1–10을 정밀 crop하는 재현 스크립트

## 번역 범위

초록, 색인어, 본문 I–V, 감사의 글, 부록 A, 표 1–4 및 A1–A2, 그림 1–10과 캡션, 식 (1)–(28), 참고문헌 [1]–[51], 저자 약력 4개를 포함한다.

## 조판 및 검수

- 원문 전체 17쪽과 대응하는 최종본 **18쪽**
- 그림 **10개**, HTML 표 **6개**, 표시 수식 블록 **28개**
- 식 (1)–(28)은 첨자·분수·합·벡터·제약조건 정렬을 보존한 벡터 수식으로 조판
- 원문 페이지 통 캡처를 사용하지 않고 그림 영역만 정밀 crop하여 삽입; 축·범례·패널 전체를 보존하고 원문 영문 캡션은 제외
- 넓은 그림과 6열 이상 표는 2단 전체 폭으로 배치
- `check_multicol_layout.py` 정적 검사 통과
- `validate_output.py --final` 결과: **PASS — 모든 검사 통과**
- 전체 18쪽 contact-sheet 및 수식/그림 문제 페이지 확대 시각 QA 완료: 빈 페이지, 잘림, 겹침, 표 overflow, 중복 영문 캡션 없음

## 체크섬

```text
79402b8345249bea9dd2fe96360f7a3fefd3f15503651b8d67b4f535ba13e513  2506.22579_ko_translation_layout.pdf
b166c871038df931670d22d65aa0b8a6809581d3b4b44f689547a639e42ffc8c  translation.html
3173e1bb584ba52693f9330925610a5100432ef0e986637ea40f5d852abf3fdf  original.pdf
```

## 재생성

```bash
uv run --with pymupdf python3 extract_clean_figures.py
python3 render_equations.py
python3 build_translation.py
python3 ../../../scripts/render_pdf.py translation.html 2506.22579_ko_translation_layout.pdf
uv run --with pymupdf python3 ../../../scripts/validate_output.py . \
  --final 2506.22579_ko_translation_layout.pdf
```

> 본 번역은 연구·검토 편의를 위한 비공식 한국어 번역이다. 인용 및 법적 해석에는 DOI의 영어 원문을 기준으로 한다.
