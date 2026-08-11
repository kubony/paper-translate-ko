# Action-to-Action Flow Matching (arXiv:2602.07322v2) 한국어 전문 번역

**작성·번역·조판:** 제니 (Jennie)

## 산출물

- `2602.07322_ko_translation_selectable_compat.pdf` — 15쪽 A4 2단 한국어 완역 PDF(텍스트 선택·검색 가능, viewer 호환본)
- `2602.07322_ko_translation_part1_pages01-08.pdf` / `part2_pages09-15.pdf` — Discord 전달용 무손실 분할본
- `translation.html` — 인쇄용 2단 HTML
- `translation.md` — 초록부터 부록까지 한국어 전문 원고
- `manifest.json` — figure/table/equation inventory
- `citation_map.json` — 42개 참고문헌 숫자 인용 매핑
- `source/` — arXiv v2 active LaTeX source와 원문 figure 자산
- `assets/videos.json`, `assets/videos/thumbs/` — 공식 프로젝트 영상 13개의 출처·원격 보관 URL과 썸네일
- `qa_last_contact_sheet.jpg` — 최종 15쪽 전체 시각 QA contact sheet

## 번역 범위

arXiv v2 active LaTeX source를 기준으로 초록부터 부록 A까지 완역했다. Figure 1–11·S1–S8(19개), table 1–2·S1(3개), display equation 1–6, 참고문헌 42개를 보존했다. LaTeX 주석과 비활성 초안은 제외했다.

## 검증

- 출력 계약 validator: **PASS**
- figure cross-reference: **PASS** — source label→번호·href·참조 횟수 일치
- citation validator: **PASS** — 본문 인용 59회, 참고문헌 42개, 내부 링크 87개
- 2단 layout static preflight: **PASS**
- 최종 PDF: 15쪽 A4, 원문 20쪽 대비 0.75배
- 인벤토리: figure 19, table 3, display equation 6, reference 42, official video 13
- selectable compatibility layer: 최소 page text ratio 0.9992, link annotation 226개
- outline-only viewer PDF와 selectable PDF의 전 페이지 raster pixel: 15/15 동일
- Discord 분할본과 통합본의 page text·raster pixel·link count: 15/15 동일
- 전 페이지 시각 QA: 빈 페이지·잘림·겹침·2단 흐름 오류 없음; 마지막 page에 영상 13개 카드 모두 수록

## SHA-256

- 통합 PDF: `546b4168592537fdb2469a92e1ec9a8626930ad98d54e6e9794af7e681cf47a0`
- HTML: `d06bc89c4bf13fd97fcac99ea39261f15f1fd9854cacf05fcd8be14a8c6c7b8d`

## 출처

- arXiv: https://arxiv.org/abs/2602.07322
- 원문 PDF: https://arxiv.org/pdf/2602.07322v2
- 프로젝트: https://lorenzo-0-0.github.io/A2A_Flow_Matching/
