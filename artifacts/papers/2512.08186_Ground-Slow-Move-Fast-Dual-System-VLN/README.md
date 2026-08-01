# DualVLN (arXiv:2512.08186) 한국어 전문 번역

## 산출물

- `translation.html` — 초록부터 본문, 결론, 기여/감사, 전체 부록까지 수록한 2단 A4 한국어 전문 번역
- `2512.08186_ko_translation_layout_v2.pdf` — 교정 2판 고해상도 PDF
- `2512.08186_ko_translation_layout_v2_delivery.pdf` — Discord 전달용 교정 2판 PDF
- `manifest.json` — section, figure, table, display equation inventory와 원문 source 대응표
- `figures/assets/*.png` — 원문 `source/images/*.pdf`에서 개별 변환한 figure 자산 14개
- `original.pdf` — 대조에 사용한 원문 PDF(17쪽)

## 교정 2판 — 2026-08-01

사용자 검토를 반영해 3.1절을 원문 의미 슬롯에 맞춰 다시 번역했다.

- `self-directed view adjustment`를 camera 방향과 pixel-goal 출력 사이의 반복적 선택 과정으로 명시했다.
- `informative perspectives`의 직역인 “정보성 높은 관점”을 “목표를 판별하기에 적합한 시야”로 수정했다.
- `farthest pixel goal grounding`을 현재 시야에서 확인 가능한 trajectory point 가운데 agent로부터 가장 먼 point를 예측하는 문제로 풀어 썼다.
- depth와 camera–point distance의 비교가 occlusion 판정에 사용된다는 인과관계를 명시했다.
- Backbone 표기를 `Qwen2.5-VL`로 통일하되 원 논문이 사용한 모델 버전은 변경하지 않았다.

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
