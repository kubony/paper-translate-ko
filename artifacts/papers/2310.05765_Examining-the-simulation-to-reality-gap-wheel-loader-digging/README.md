# Examining the simulation-to-reality gap of a wheel loader digging in deformable terrain

arXiv: [2310.05765v3](https://arxiv.org/abs/2310.05765v3) 논문의 한국어 전문 번역 산출물이다.

## 최종 산출물

- [`2310.05765_ko_translation_layout.pdf`](./2310.05765_ko_translation_layout.pdf) — A4 2단 한국어 완역 PDF, 19쪽
- [`translation.html`](./translation.html) — PDF 생성에 사용한 전체 번역 HTML
- [`original.pdf`](./original.pdf) — arXiv 원문 PDF, 22쪽
- [`metadata.json`](./metadata.json) — arXiv 메타데이터

## 구성

- 제목·저자·초록
- 본문 1–9절
- 보충 자료와 부록 보충 그림
- 감사의 글
- 참고문헌 49개
- 원문 Figure 15개와 Table 5개
- 표시 수식 9개

그림은 원문 페이지 전체 캡처가 아니라 각 Figure 영역만 잘라 삽입했으며, 표는 이미지가 아닌 HTML 표로 재구성했다. 수치·단위·변수명·시뮬레이터 충실도 이름(D50–G400)은 원문 표기를 유지했다.

## 재현

```bash
python3 build_translation.py
python3 ../../../scripts/render_pdf.py translation.html 2310.05765_ko_translation_layout.pdf
```

레포 루트에서 실행할 경우:

```bash
python3 artifacts/papers/2310.05765_Examining-the-simulation-to-reality-gap-wheel-loader-digging/build_translation.py
python3 scripts/render_pdf.py \
  artifacts/papers/2310.05765_Examining-the-simulation-to-reality-gap-wheel-loader-digging/translation.html \
  artifacts/papers/2310.05765_Examining-the-simulation-to-reality-gap-wheel-loader-digging/2310.05765_ko_translation_layout.pdf
```

## 검증 결과

`validate_output.py` 최종 판정: **PASS(위반 없음, 경고 1건)**

- Figure 15/15
- Table 5/5
- 표시 수식 9/9
- 이미지 상대경로 및 파일 존재 확인
- LaTeX 잔재·미번역 영어 블록·템플릿 placeholder 없음
- 페이지 통 캡처 없음
- PDF 19쪽 / 원문 22쪽(정상 범위)
- 경고 1건은 수치가 없는 정성적 측정량 표(Table 1)에 대한 일반 휴리스틱 경고이며, 원문 구조와 일치한다.

시각 QA contact sheet는 [`qa_translation_pages.jpg`](./qa_translation_pages.jpg)에 보존했다.
