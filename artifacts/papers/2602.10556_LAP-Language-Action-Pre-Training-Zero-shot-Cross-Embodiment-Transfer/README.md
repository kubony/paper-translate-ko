# LAP: Language-Action Pre-Training — 한국어 전문 번역

- **작성자:** 제니 (Jennie)
- **원문:** [arXiv:2602.10556v2](https://arxiv.org/abs/2602.10556v2)
- **프로젝트:** [lap-vla.github.io](https://lap-vla.github.io/)
- **코드:** [lihzha/lap](https://github.com/lihzha/lap)
- **번역 기준일:** 2026-07-27

## 범위

초록, 본문 1–5절, 감사의 말, 전체 부록, 그림 1–12, 표 1–5, display equation 9개, 참고문헌 요약을 한국어로 재구성한다. 프로젝트 페이지 영상 32개는 썸네일과 원본·보관 링크를 제공한다.

## 파일

- `original.pdf`: arXiv v2 원문
- `2602.10556_ko_translation_layout.html`: 한국어 전문 번역 HTML
- `2602.10556_ko_translation_layout.pdf`: 한국어 전문 번역 PDF
- `manifest.json`: 필수 구조 inventory
- `source/`: arXiv e-print LaTeX 원문 및 figure
- `figures/final/`: PDF 삽입용 figure 1–12
- `assets/videos.json`: 프로젝트 영상 원본 URL, 로컬/GCS 경로, checksum

## 번역 원칙

VLA, policy, action, action chunk, flow matching, cross-embodiment, embodiment, fine-tuning, zero-shot 등 핵심 전문용어는 영문을 유지하거나 한국어와 병기한다. 모델·데이터셋·수치·단위는 원문 표기를 보존한다.
