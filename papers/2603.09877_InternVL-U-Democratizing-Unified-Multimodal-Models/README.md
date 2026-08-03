# InternVL-U 한국어 전문 번역

**작성자: 제니**

## 대상

- 논문: *InternVL-U: Democratizing Unified Multimodal Models*
- arXiv: [2603.09877](https://arxiv.org/abs/2603.09877)
- 기준 버전: v1, 2026-03-10
- 원문 분량: 61쪽

## 산출물

- `2603.09877_ko_translation_layout.pdf` — 한국어 전문 번역 PDF(53쪽, 2단 학술 레이아웃)
- `translation.html` — PDF 렌더링 원본 HTML
- `merged_translation.md` — 통합 번역 Markdown
- `original.pdf` — arXiv 원문 PDF
- `source/` — arXiv LaTeX 원본
- `manifest.json` — 피겨·표·디스플레이 수식 inventory
- `validation.txt` — 최종 자동 검증 결과

## 번역 범위와 편집 원칙

초록, 서론, 관련 연구, 방법론, 데이터 구축, 실험, 결론, TextEdit 벤치마크 부록, 과학·컴퓨터과학·입체기하 데이터 구축 부록을 번역했다. 원문 모델명·데이터셋명·벤치마크명·지표명·수치·단위를 유지하고, 원문 피겨 29개, 표 24개, 디스플레이 수식 14개를 반영했다. 참고문헌 340개는 제목을 원문 표기로 유지했다.

## 검증

- `check_multicol_layout.py`: PASS
- `validate_output.py`: PASS(위반 0건, 인라인 `[n]` 휴리스틱 경고 1건)
- 최종 PDF: 53쪽 / 원문 61쪽(0.87배)
- 이미지 경로·파일: 29/29 존재
- 표: 24/24
- 디스플레이 수식: 14/14
- 전 53쪽 렌더링 및 contact-sheet 시각 QA 완료
- 페이지 경계 clipping 검사: 이상 없음

## 재생성

```bash
uv run --with markdown python3 build_internvlu.py
uv run --with pymupdf python3 \
  ~/.hermes/skills/research/paper-translate-ko/scripts/convert_pdf_figures_for_html.py \
  translation.html --root . --out-dir figures/rendered --scale 2.2
python3 ~/.hermes/skills/research/paper-translate-ko/scripts/render_pdf.py \
  translation.html 2603.09877_ko_translation_layout.pdf
uv run --with pymupdf python3 \
  ~/.hermes/skills/research/paper-translate-ko/scripts/validate_output.py \
  . --final 2603.09877_ko_translation_layout.pdf
```
