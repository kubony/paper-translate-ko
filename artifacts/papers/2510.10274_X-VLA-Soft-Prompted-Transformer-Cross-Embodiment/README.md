# X-VLA (arXiv:2510.10274) 한국어 전문 번역

**원제**: *X-VLA: Soft-Prompted Transformer as Scalable Cross-Embodiment Vision-Language-Action Model*
**저자**: Jinliang Zheng·Jianxiong Li 외 13인 (Institute for AI Industry Research (AIR), Tsinghua University · Shanghai AI Lab · Peking University)
**출처**: preprint / technical report, 33페이지 · 1차 카테고리 `cs.RO` (`cs.AI`, `cs.CV`)
**게재일**: 2025-10-11 · **번역 생성일**: 2026-07-27
**프로젝트**: https://thu-air-dream.github.io/X-VLA/

---

## 1. 산출물

| 파일 | 설명 |
|------|------|
| `translation.html` | 초록부터 부록·기여/감사의 글까지 전 문단을 한국어로 완역한 **독립 실행형 2단 HTML**. 모든 그림·표·수식·참고문헌 포함. |
| `manifest.json` | 구조 메타데이터(섹션/그림/표/수식/참고문헌 실제 카운트 및 완결성 체크). |
| `README.md` | 본 문서. |
| `figures/assets/*.png` | `source/Figures/`의 개별 PDF/PNG 자산을 브라우저 표시용 PNG로 변환한 14개 그림. |

번역은 원문 LaTeX 소스(`source/main.tex` 1312행, `source/main.bbl` 95개 항목)와 `metadata.json`, `original.pdf`를 직접 대조해 작성했다.

## 2. 번역 원칙

- **문체**: 한국어 문어체 평서형(`~한다`). 요약 없이 모든 비주석 원문 문단을 완역.
- **용어 혼합 표기**: `VLA, policy, action, controller, flow matching, Diffusion Transformer(DiT), embodiment, cross-embodiment, soft prompt, backbone, PEFT` 등 핵심 기술 용어는 한국어에 영문을 혼합해 표기.
- **고유명 유지**: 모델명·벤치마크명·데이터셋명·지표명(X-VLA, π₀, Florence, LIBERO, Simpler, RoboTwin-2.0, NAVSIM, AGIBOT, Droid, RoboMind 등)은 원문 표기 유지.
- **수식**: `<pre class="equation">`의 ASCII/유니코드 근사로 원식과 번호 `(1)~(6)`을 보존. 주요 수식은 `explain-card`로 평문 해설 추가.
- **표**: 이미지가 아니라 HTML `<table>`로 재구성하며 모든 행·열·수치·강조(굵게/색)를 보존. 원문의 <span style="color:green">녹색</span>/<span style="color:red">적색</span>/회색 효과 표기를 색으로 재현.
- **그림**: 원문 페이지 통캡처가 아니라 `source/Figures/`의 개별 자산을 상대경로 `figures/assets/…`로 삽입.
- **인용**: 본문 인라인 인용 번호는 제거하되 인용된 방법·데이터셋 명칭은 문장에 유지. 참고문헌은 95개 항목 전체를 저자·연도·원문 제목으로 목록화.

## 3. 구조 / 검증 카운트

| 항목 | 수 |
|------|----|
| 본문 번호 섹션 | 6 (Introduction, Preliminary, Heterogeneous Soft Prompt Learning, X-VLA, Experiments, Conclusion) |
| 부록 섹션 | 15 (A~O) |
| 서브섹션 | 8 (4.1, 4.2, 5.1~5.3, D.1~D.3) |
| 서브서브섹션 | 2 (4.2.1, 4.2.2) |
| 그림 | 14 (전부 개별 자산·상대경로) |
| 표 | 16 (전부 HTML table) |
| 디스플레이 수식 | 6 (번호 보존) |
| 참고문헌 | 95 |

핵심 수치 검증 예: 표 2에서 **X-VLA (Ours, 0.9B)** — Simpler VM 80.4 / VA 75.7 / WidowX 95.8, LIBERO Avg 98.1, RoboTwin-2.0 Easy 70.0 / Hard 39.0, VLABench 51.1, NAVSIM PDMS 87.3.

## 4. 여는 법

```bash
# 어떤 브라우저로든 열면 된다 (외부 의존성 없음).
xdg-open translation.html      # Linux
# 또는
open translation.html          # macOS
```

- `translation.html`은 완결된 단일 파일이며, 그림만 `figures/assets/` 상대경로를 참조하므로 두 경로를 함께 유지해야 한다.
- 인쇄(Ctrl/Cmd+P) 시 A4 2단 레이아웃으로 PDF 저장이 가능하다(`@page` 및 `print-color-adjust` 설정 포함).
- 그림은 `source/Figures/`의 PDF를 `pdftoppm`으로 PNG 변환해 넣었으므로 PDF 뷰어 없이도 표시된다.

## 5. 그림 자산 매핑

`intro_small`(그림1), `compare_with_others`(2), `data_mixture`(3), `line_plot_scaling_steps`(4), `scaling`(5), `all_bench`(6), `real_exp`(7), `tsne`(8), `prompt_comparison`(9), `archi`(10), `softfold`(11), `fold`(12), `widowx_tasks`(13), `all_setup`(14).
