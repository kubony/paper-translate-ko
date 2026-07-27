# Leave No Observation Behind / A2C2 — 한국어 전문 번역

- **원문 제목:** Leave No Observation Behind: Real-time Correction for VLA Action Chunks
- **저자:** Kohei Sendai, Maxime Alvarez, Tatsuya Matsushima, Yutaka Matsuo, Yusuke Iwasawa
- **소속:** The University of Tokyo
- **원문:** [arXiv:2509.23224](https://arxiv.org/abs/2509.23224)
- **번역 기준일:** 2026-07-27

## 번역 범위

초록부터 본문 1–7절, Ethics Statement, Reproducibility Statement, 전체 Appendix, 참고문헌까지 문단 단위로 완역했다. 원문 figure 7개(개별 image asset 20개), table 8개, display equation 10개를 모두 재삽입·재구성했다. 표는 이미지가 아닌 HTML table로 작성해 수치와 원문 강조를 보존했다.

## 파일

- `translation.html`: template 기반 A4 2단 한국어 전문 번역
- `manifest.json`: section·figure·table·equation·reference inventory
- `original.pdf`: 원문 PDF(17쪽)
- `source/arxiv.tex`, `source/sections/*.tex`: 번역 대조에 사용한 LaTeX 원문
- `source/figures/`: 원문 개별 figure asset
- `source/figures/concept_figure.png`, `Kinetix.png`, `residual_transformer.png`: 브라우저 삽입을 위해 원문의 vector PDF figure를 PNG로 변환한 자산

## 번역 원칙

- 요약이 아닌 전체 문단 번역이며 문어체 평서형으로 작성했다.
- VLA, policy, action chunking, RTC, correction head, latency, horizon, inference 등 핵심 기술어는 영문 혼합 표기를 유지했다.
- model·benchmark·dataset 이름, 수치, 단위, 수식 기호를 원문대로 보존했다.
- 원문 페이지 통캡처는 사용하지 않고 개별 figure asset만 상대경로로 삽입했다.
- 수식은 `<pre class="equation">`의 ASCII/Unicode 근사 표기로 재현했다.
- 참고문헌 30개는 원문 제목을 유지한 목록으로 수록했다.

## 열람

브라우저에서 `translation.html`을 열면 된다. 모든 image 경로는 이 디렉터리를 기준으로 한 상대경로다. 인쇄 시 A4 2단 레이아웃이 적용된다.
