# DualVLN 한국어 전문 번역 3판 원문 대조 감사 기록

- **대조·교정 기준일:** 2026-08-02
- **원문:** `source/iclr2026_conference.tex`, `source/sections/0_abstract.tex`–`7_appendix.tex`, `source/tables/*.tex`, `original.pdf`
- **3판 산출물:** `translation_v3.html`
- **보존한 기존 번역:** `translation.html`
- **적용 기준:** 문어체 평서형, active LaTeX 본문 전체 번역, 수치·수식·그림·표·참고문헌 보존, VLA/robotics 용어집 및 DualVLN-specific translation rules

## 섹션별 문단 대조 결과

| 섹션 | 원문 대조 | 핵심 교정 사항 |
|---|---:|---|
| 표지·번역 메모 | 완료 | subtitle을 **“한국어 전문 번역 · 전면 재번역 3판”**으로 변경했다. 번역 생성일과 3판 교정일을 2026-08-02로 기록했다. 3판에서 구분한 pixel/latent goal, plan-anchor/current RGB, DINOv2 patch feature, Q-Former, Social-VLN/HCR 규칙을 명시했다. |
| 초록 | 완료 | `synergistically integrates`를 상호보완적 결합으로 옮겼다. System 2의 중기 waypoint grounding과 System 1의 trajectory 생성을 각각 분명한 주체로 썼다. 학습 분리의 효과와 현실 실험 결과를 과장 없이 원문 범위로 한정했다. |
| 그림 1 | 완료 | `high-frequency RGB`를 영상의 공간 주파수가 아니라 **빠른 실행 주기마다 갱신되는 RGB 조건**으로 풀었다. 2 Hz/30 Hz와 비동기 inference의 역할을 보존했다. |
| 1. 서론 | 완료 | VLM 호출이 action step마다 발생해 latency가 커지는 논리를 자연스럽게 재구성했다. System 2 선행 훈련·파라미터 고정과 이후 latent-query/System 1 훈련을 분리했다. explicit pixel goal과 implicit latent goal의 역할을 혼동하지 않도록 교정했다. |
| 2. 관련 연구 | 완료 | text action, pixel grounding+별도 실행 module, direct latent-to-trajectory, synchronous/async dual-system의 차이를 명확히 했다. `high-frequency decision-making`을 빠른 의사결정 주기로 옮겼다. |
| 3. 방법 개요·그림 2 | 완료 | System 2는 global planning 및 grounded target 제공, System 1은 비동기 latent와 현재 관측을 조건으로 continuous trajectory 생성이라는 역할 분담을 명시했다. |
| 3.1 System 2 | 완료 | self-directed view adjustment를 camera를 먼저 바꿀지 현재 frame에서 pixel goal을 출력할지 반복 선택하는 동작으로 풀었다. farthest pixel goal은 **현재 시야에 보이는 trajectory point 중 agent에서 가장 먼 point**로 정의했다. `distance > depth`인 point는 다른 표면 뒤에 가려져 제외된다고 명시했다. 이 depth 사용은 offline 학습-label filtering임을 분리했다. |
| 3.2 System 1 | 완료 | System 2 context `X`, learnable query `Z`, latent goal `Z′`의 생성 주체를 구분했다. RGB 두 시점은 고정 plan-anchor와 해당 tick의 최신 current RGB이며 누적 history가 아님을 명시했다. DepthAnythingV2-Small의 DINOv2 visual trunk가 patch feature를 만들며 CLS/global token 및 depth decoder 출력과 구분했다. `fuse`는 두 시점 patch token의 self-attention 결합으로, Q-Former는 32 learned query가 fused memory를 cross-attention하여 32개 새 요약 token을 합성하는 과정으로 교정했다. Q-Former token 수 32와 trajectory horizon 32의 일대일 대응을 부정했다. |
| 3.2 Flow Matching | 완료 | 수식 (1)–(3), 변수, 기호와 번호를 보존했다. noise/timestep sampling이 runtime이 아니라 System 1 **학습 step**에서 수행됨을 명시했다. |
| 3.3 구현 세부사항 | 완료 | System 2의 한 epoch full finetuning과 System 1의 후속 학습을 분리했다. Qwen 계열 명칭을 Qwen2.5-VL로 통일했다. RGB encoder를 DepthAnythingV2의 DINOv2 ViT visual trunk로 특정하되 depth decoder/runtime depth condition이라는 잘못된 함의를 제거했다. |
| 4. Social-VLN | 완료 | 평가 benchmark에서는 Habitat 3.0 humanoid를 GT route 주변에 배치하고, humanoid가 통로를 영구 봉쇄하지 않는지 episode를 검수한다고 명시했다. 그림 3은 독립 metric이 아닌 정성적 interaction scenario inventory로 설명했다. HCR은 원문이 분모·contact threshold·집계 단위를 정의하지 않으므로 임의 공식을 추가하지 않았다. 763K 학습-data modified-A* pipeline은 benchmark curation과 별개로 분리했다. |
| 5.1 Simulation 실험 | 완료 | VLN-CE와 VLN-PE의 평가 조건 및 지표 정의를 자연스러운 문장으로 재작성했다. 표 1의 baseline 세 범주를 분리했다. 표 2의 DualVLN은 VLN-PE trajectory로 fine-tuning하지 않은 zero-shot transfer 조건임을 분명히 했다. Social-VLN 성능 하락은 평가 결과로만 서술했다. |
| 5.2 현실 실험 | 완료 | 센서 stream, remote-server inference, odometry 변환, MPC tracking의 runtime 순서를 명시했다. RGB-D 전송과 System 1 visual encoder의 depth decoder 사용 여부를 구분했다. System 2 KV-cache latency와 System 1 TensorRT trajectory 생성을 각각의 runtime 최적화로 옮겼다. |
| 5.3 Ablation | 완료 | `w/o Sys.2 Train`, `w/o Pixel Goal`, `w/o Latent Goal`의 학습/평가 조건을 각각 분리하여 direct System 1 condition과 혼동하지 않도록 했다. Point-goal 변형의 추가 depth는 평가용 modular 변형임을 명시했다. Data scaling과 pixel-goal/trajectory consistency 분석의 표본·metric·저자 해석을 원문 범위로 유지했다. |
| 6. 결론 | 완료 | 원문보다 강한 인과 주장 없이 기여와 기대를 저자 관점으로 옮겼다. |
| 기여 및 감사의 말 | 완료 | 역할별 기여자와 지원 기관, InternVLA-N1/InternNav 협력자 전체를 보존하고 직역투를 교정했다. |
| 부록 A.1 | 완료 | System 2 Stage 1의 세 출력 유형, action set, prompt, 최대 4-turn chunk, farthest successfully projected waypoint, STOP supervision, optimizer·batch·step을 대조했다. |
| 부록 A.2 | 완료 | 32 waypoint interpolation, 4개 `<TRAJ>` query, 코드 block, Qwen2.5-VL 고정, latent query+DiT만 업데이트하는 Stage 2를 대조했다. “end-to-end”가 고정 VLM까지 재훈련한다는 뜻이 아님을 밝혀 단계 혼동을 제거했다. |
| 부록 B | 완료 | historical video frame/current observation 및 layer별 attention 서술을 대조했다. attention weight를 물체 확률이나 인과적 중요도로 단정하지 않는 해석상 주의를 덧붙였다. |
| 참고문헌 | 완료 | 기존 참고문헌 제목·순서·항목을 변경하지 않았다. |

## Inventory 및 구조 보존 검증

2026-08-02에 `translation.html`과 `translation_v3.html`을 기계 비교했다.

| 항목 | 기존 | 3판 | 결과 |
|---|---:|---:|---|
| `<figure>` | 11 | 11 | 일치 |
| `<img>` | 14 | 14 | 일치 |
| `<table>` | 4 | 4 | HTML block 전체 일치 |
| equation `<pre class="equation">` | 3 | 3 | 내용·번호 전체 일치 |
| 전체 `<pre>` | 11 | 11 | 개수 일치 |
| 참고문헌 `<ol class="refs">` | 1 | 1 | block 전체 일치 |
| asset 경로 | 14 | 14 | 순서·문자열 일치, 누락 파일 0개 |
| `<h2>` / `<h3>` / `<h4>` | 12 / 18 / 25 | 12 / 18 / 25 | 일치 |

- 기본 여닫는 tag(`html`, `head`, `body`, `section`, `div`, `p`, `figure`, `figcaption`, `table`, `pre`, `ol`, `ul`)의 개수가 모두 균형을 이룬다.
- 표의 숫자·행·열·강조를 포함한 네 table block은 기존 HTML과 byte-level 문자열 비교에서 동일하다.
- 그림 asset 목록은 다음 14개 경로를 그대로 유지하며 모두 실제 파일이 존재한다: `teaser.png`, `framework.png`, `socialvln_action.png`, `socialvln.png`, `exp_realworld_v2.png`, `qualitative_real2.png`, `ablate_goal_v2.png`, `goals.png`, `exp_ablation_data.png`, `corr_plot.png`, `attention_text1.png`, `attention_image1.png`, `attention_text2.png`, `attention_image2.png`(모두 `figures/assets/` 아래).
- 기존 `translation.html` SHA-256은 작업 전후 **`99da586e15f645bac3fb99ba270c15d1c29c8640f2711d47d2077c1d03c87375`**로 보존되었다.

## 최종 판정

- **초록–부록 active LaTeX 본문 문단 대조:** 완료
- **직역투 및 역할 주체 교정:** 완료
- **학습/평가/runtime 단계 분리 교정:** 완료
- **figure/table/equation/reference inventory 보존:** 완료
- **asset 경로 유효성:** 완료(누락 0개)
