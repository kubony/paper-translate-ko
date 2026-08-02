# DualVLN (arXiv:2512.08186) 한국어 전문 번역

**작성·교정:** 제니

## 권장 산출물 — 전면 재번역 3판

- `translation_v3.html` — 대화에서 확정한 개념 구분과 원문 충실도 감사를 반영한 3판 HTML
- `2512.08186_ko_translation_layout_v3.pdf` — 16쪽 고해상도 PDF
- `2512.08186_ko_translation_v3_delivery.pdf` — Discord 전달용 압축 PDF
- `v3_translation_audit.md` — 원문 section·paragraph 대조 기록
- `v3_fidelity_audit.md` — 원문보다 강한 주장 18건의 식별 및 18/18 수정 기록
- `manifest.json` — section, figure, table, display equation inventory와 source 대응표
- `figures/assets/*.png` — 원문 figure 자산 14개
- `original.pdf` — 대조에 사용한 원문 PDF(17쪽)

기존 `translation.html`과 `*_v2*.pdf`는 교정 2판 기록으로 보존한다.

## 전면 재번역 3판 — 2026-08-02

사용자와의 후속 질의에서 드러난 모호성을 반영해 active LaTeX 본문 전체를 문단 단위로 다시 대조했다.

- 초록의 기능적 개괄과 방법 수식의 직접 condition `Z′ ⊕ F`를 구분했다.
- System 1의 원문 직접 서술은 time `t`의 System 2 마지막 RGB와 `t+k`의 current RGB, ViT, self-attention fusion, Q-Former 32-token 압축까지로 제한했다.
- 공개 구현에서 확인한 DINOv2 patch/CLS, current history 비누적, LoaderDrive 대조 내용은 **논문 본문 아님**이 표시된 구현 대조 메모로 분리했다.
- pixel-goal label 생성에 쓰는 simulator depth, DepthAnythingV2-Small의 ViT backbone, 현실 runtime RGB-D stream, System 1 depth conditioning을 서로 혼동하지 않도록 했다.
- Social-VLN benchmark curation과 763K training-data pipeline을 분리했다.
- `agent가 경로를 완전히 막는다`의 주체가 배치된 humanoid임을 문맥상 분명히 했다.
- HCR은 원문이 제시한 범위까지만 번역하고, 산식·분모·contact threshold·episode/step 집계가 원문 제공 범위에 없다는 사실은 별도 원문 대조 메모로 분리했다.
- attention weight에 대한 번역자의 일반적 해석 경고를 저자 본문에 섞지 않았다.

## 검증

- 원문 충실도 감사: **18/18 RESOLVED**
- `validate_output.py` 작업폴더+PDF gate: **PASS**
- delivery PDF 소급 gate: **PASS**
- HTML structure: figure 11, image asset 14, table 4, display equation 3, heading 구조 보존
- 페이지: 원문 17쪽, 3판 16쪽(validator 정상 범위)
- 전체 16쪽 contact-sheet 시각 QA: **PASS**
- 사용자 제보로 발견한 Chrome multicol의 wide-table H3 제목 분할을 수정했다. `h3.section`에도 `column-span: all`을 적용하고 표 1~4 제목과 p12를 150 dpi로 재검증했다.
- delivery PDF p2·p7·p9·p12·p16 압축 후 시각 QA: **PASS**

## 번역 기준

- 기준 source: `source/iclr2026_conference.tex`, `source/sections/*.tex`, `source/tables/*.tex`
- 시각 구조 확인: `original.pdf`
- 주석 처리된 초안/삭제 문장은 제외하고 실제 컴파일되는 본문을 번역했다.
- 본문 번역에는 원문이 직접 말한 수준만 남기며, 구현 확인과 번역자의 비평은 출처·범위를 밝힌 별도 메모로 분리한다.
- 문체는 문어체 평서형(`~한다`)을 사용한다.
- VLA, policy, action, controller, flow matching, Diffusion Transformer, pixel goal, latent feature, embodiment, cross-embodiment 등은 영문 혼합 표기를 유지한다.
- 표 4개는 HTML table로 재구성하여 수치와 bold 강조를 보존한다.
- display equation 3개는 ASCII/Unicode 근사식으로 한 벌씩만 수록한다.
- 원문 figure 11개는 페이지 통캡처가 아닌 개별 자산으로 삽입한다.
- 본문 citation 번호는 생략하고 인용 문헌의 영문 제목을 유지한 참고문헌 목록을 수록한다.

## Inventory

| 항목 | 개수 |
|---|---:|
| 번역 section(초록·기여/감사·부록 포함) | 10 |
| Figure | 11 |
| Figure asset | 14 |
| HTML table | 4 |
| Display equation | 3 |
| 참고문헌 목록 | 54 |

## SHA-256

- 고해상도 PDF: `fe9131b3f8ae1f3d82243960d16dd69a0da538965c1fec55b8721d6a083ae14d`
- delivery PDF: `6f7193be4ddac840b53fd2c85e6e991b2831eda53f788c09867a44f23fc2f3fa`
- HTML: `0604dbfe9e1064f5cc500d51965c2fa5954a2418e9018f5425e40a1fcda61b2c`

## 열람

브라우저에서는 `translation_v3.html`을 연다. 모든 image 경로는 작업 디렉터리 기준 상대경로이며, 인쇄 시 A4 2단 레이아웃이 적용된다.
