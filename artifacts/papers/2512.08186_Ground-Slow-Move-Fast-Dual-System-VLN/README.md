# DualVLN (arXiv:2512.08186) 한국어 전문 번역

## 산출물

- `translation.html` — 초록부터 본문, 결론, 기여/감사, 전체 부록까지 수록한 2단 A4 한국어 전문 번역
- `manifest.json` — section, figure, table, display equation inventory와 원문 source 대응표
- `figures/assets/*.png` — 원문 `source/images/*.pdf`에서 개별 변환한 figure 자산 14개
- `original.pdf` — 대조에 사용한 원문 PDF(17쪽)

## 번역 기준

- 기준 source: `source/iclr2026_conference.tex`, `source/sections/*.tex`, `source/tables/*.tex`
- 시각 구조 확인: `original.pdf`
- LaTeX에서 주석 처리된 초안/삭제 문장은 번역 대상에서 제외하고, 실제 컴파일되는 본문을 완역했다.
- 문체는 문어체 평서형(`~한다`)을 사용했다.
- VLA, policy, action, controller, flow matching, Diffusion Transformer, pixel goal, latent feature, embodiment, cross-embodiment 등은 영문 혼합 표기를 유지했다.
- 표 4개는 이미지가 아닌 HTML table로 재구성하여 수치와 bold 강조를 보존했다.
- display equation 3개는 `pre.equation`에 ASCII/Unicode 근사식으로 한 벌씩만 수록했다.
- 원문 figure 11개는 페이지 통캡처가 아닌 개별 자산으로 삽입했다. 부록 그림 11은 원문의 네 panel을 네 개별 asset으로 구성했다.
- 본문 citation 표시는 생략했으며, 인용된 문헌의 영문 제목을 유지한 참고문헌 목록을 말미에 수록했다.

## Inventory

| 항목 | 개수 |
|---|---:|
| 번역 section(초록·기여/감사·부록 포함) | 10 |
| Figure | 11 |
| Figure asset | 14 |
| HTML table | 4 |
| Display equation | 3 |
| 참고문헌 목록 | 54 |

세부 source 대응은 `manifest.json`을 참조한다.

## 열람

브라우저에서 `translation.html`을 연다. 모든 image 경로는 작업 디렉터리 기준 상대경로다. 인쇄 시 A4, 2단 레이아웃이 적용된다.
