# InternVL-U 한국어 전문 번역

**작성자: 제니**

## 대상

- 논문: *InternVL-U: Democratizing Unified Multimodal Models*
- arXiv: [2603.09877](https://arxiv.org/abs/2603.09877)
- 기준 버전: v1, 2026-03-10
- 원문 분량: 61쪽

## 산출물

- `2603.09877_ko_translation_layout.pdf` — 한국어 전문 번역 PDF(49쪽, 2단 학술 레이아웃, 숫자형 인용 링크)
- `translation.html` — PDF 렌더링 원본 HTML
- `merged_translation.md` — 통합 번역 Markdown
- `original.pdf` — arXiv 원문 PDF
- `source/` — arXiv LaTeX 원본
- `manifest.json` — 피겨·표·디스플레이 수식 inventory
- `validation.txt` — 최종 자동 검증 결과

## 번역 범위와 편집 원칙

초록, 서론, 관련 연구, 방법론, 데이터 구축, 실험, 결론, TextEdit 벤치마크 부록, 과학·컴퓨터과학·입체기하 데이터 구축 부록을 번역했다. 원문 모델명·데이터셋명·벤치마크명·지표명·수치·단위를 유지하고, 원문 피겨 29개, 표 24개, 디스플레이 수식 14개를 반영했다. 본문에서 실제 인용한 참고문헌 136개는 원문 번호에 맞춘 압축 숫자형 링크와 저자·연도·원문 제목 목록으로 정리했다.

## 검증

- `check_multicol_layout.py`: PASS
- `validate_output.py`: PASS(위반 0건, 경고 0건)
- 최종 PDF: 49쪽 / 원문 61쪽(0.80배)
- 본문 숫자형 인용: 68개 / 참고문헌: 136개 / 깨진 내부 링크: 0개
- 이미지 경로·파일·figure ID: 29/29 존재
- 표: 24/24
- 디스플레이 수식: 14/14
- 인용 밀집 본문과 참고문헌 3쪽 확대 시각 QA 완료
- 페이지 경계 clipping·겹침 검사: 이상 없음
- SHA-256: `e2156f987f3dc9d638e272b027031db30c20d30426a1e1285a1e8cc9830a3321`

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
