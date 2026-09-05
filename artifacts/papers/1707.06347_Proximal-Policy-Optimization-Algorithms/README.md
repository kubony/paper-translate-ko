# Proximal Policy Optimization Algorithms — 한국어 전문 번역

John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, Oleg Klimov의 PPO 논문(arXiv:1707.06347v2)을 초록부터 부록 B까지 완역한 산출물이다.

- 원문 abstract: https://arxiv.org/abs/1707.06347v2
- 원문 PDF: https://arxiv.org/pdf/1707.06347v2
- 원문 버전: v2, 2017-08-28
- 번역 생성일: 2026-09-05

## 전달본

- [`1707.06347_ko_translation_layout.pdf`](1707.06347_ko_translation_layout.pdf) — A4 2단 한국어 완역 PDF, 10페이지
- [`translation.html`](translation.html) — static MathML 수식과 source figure를 포함한 재현 가능한 HTML

번역 범위는 초록, 본문 1–8절, 참고문헌 14개, 부록 A–B다. 원문의 수식 (1)–(12), Algorithm 1, 그림 1–6, 표 1–6을 모두 재현했다. policy, action, advantage, surrogate objective, clipping, rollout 등 핵심 RL 용어는 영문을 유지했다.

## 주요 파일

- `original.pdf` — arXiv 원문 PDF
- `metadata.json` — arXiv v2 서지정보
- `manifest.json` — 그림·표·display equation inventory
- `translations/part1.md` — 초록–4절
- `translations/part2.md` — 5–6절
- `translations/part3.md` — 7절–부록 B
- `figures/figure-*.png` — 원문 PDF에서 개별 추출한 그림 1–6
- `build_translation.py` — Markdown fragment를 static MathML HTML로 조립하는 build script
- `structure_report.json` — 수식·그림·표·참고문헌 구조 검사 결과
- `validation.txt` — 최종 validator 결과
- `qa/rev-2/contact-sheet.jpg` — 최종 10페이지 시각 QA contact sheet

## 검증

- validator: **PASS**
- 최종 PDF: A4, 10페이지, 2,365,677 bytes
- 최종 PDF SHA-256: `d518882c48eeed3842681ef533a74a8dfd1d9d5704f1bd7b60d674ec3adacbc3`
- 원문 PDF SHA-256: `e78feadadbdbb0b601b3c2bcc81404722cd431a489b307545f9b7bea1e8c4f5b`
- 구조: 수식 12개, 그림 6개, 표 6개, 참고문헌 14개, inline math 111개
- 전 페이지 시각 QA: 빈 페이지, overflow, 겹침, 잘림, 브라우저 header/footer 없음
- 독립 fidelity 대조: 초록–부록 B의 문단, 수식, Algorithm 1, 표 수치, 그림 캡션, 각주 1–3, 참고문헌을 원문과 대조해 PASS

## 재생성

```bash
uv run --quiet --with latex2mathml --with markdown python3 build_translation.py
python3 /home/inkeun/.hermes/skills/research/paper-translate-ko/scripts/render_pdf.py \
  translation.html 1707.06347_ko_translation_layout.pdf
```
