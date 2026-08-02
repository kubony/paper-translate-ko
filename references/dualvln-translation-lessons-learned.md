# DualVLN 번역에서 얻은 재사용 가능한 lesson learned

**작성자:** 제니

**사례:** *Ground Slow, Move Fast: A Dual-System Foundation Model for Generalizable Vision-and-Language Navigation* (arXiv:2512.08186)

**목적:** 한 논문에서 반복적으로 드러난 실패를 VLA/VLN·robotics 논문 전체에 적용 가능한 검증 규칙으로 바꾼다.

## 1. 가장 큰 교훈: 이해를 개선한 사실과 번역 본문을 분리한다

논문을 읽다가 공개 코드·downstream 구현·사용자 질의로 architecture를 더 정확히 이해할 수 있다. 그러나 그 결론이 원문에 직접 쓰여 있지 않다면 번역 본문에 소급 삽입하면 안 된다.

모든 claim을 다음 세 층으로 분류한다.

| 층 | 허용 위치 | 예 |
|---|---|---|
| Source fact | 번역 본문 | 논문 방법·수식·부록이 직접 말한 내용 |
| Implementation fact | `번역·구현 대조 메모 — 논문 본문 아님` | 공개 코드의 direct tensor input, class-token 제거, frame cache 여부 |
| Interpretation/critique | `번역·원문 대조 메모 — 논문 본문 아님` | metric 정의 부족, 초록과 method 사이의 서술 수준 차이 |

### 실패 사례

- 초록이 System 1이 explicit pixel goal과 latent feature를 활용한다고 개괄한 것을 근거로, explicit `(u,v)` coordinate가 DiT에 별도 tensor로 직접 들어간다고 강화했다.
- 공개 implementation에서 확인한 DINOv2 patch token, CLS 제외, current-frame 비누적을 일반 번역 본문에 넣었다.
- Stage 2의 `end-to-end`를 설명하면서 원문보다 강한 번역자 해설을 본문에 삽입했다.

### 재발 방지

1. source paragraph마다 `source / code / analysis` claim tag를 붙인다.
2. source body에는 `source` claim만 남긴다.
3. code claim은 정확한 file/function/tensor consumer가 확인된 경우에만 구현 메모로 이동한다.
4. 초록, 방법 수식, 부록 pseudocode, 공개 call path를 서로 대체하지 않는다. 같은 system을 다른 abstraction level에서 설명할 수 있다.
5. 전면 교정 후에는 번역자가 아닌 별도 reviewer 관점으로 unsupported-strengthening audit를 수행한다.

## 2. 명사와 mechanism을 혼동하지 않는다

### Global/CLS token vs global attention

`global token`, `class token`, `global self-attention`은 다른 개념이다.

- ViT CLS/global token을 버렸다는 사실은 patch token끼리 global attention하지 않는다는 뜻이 아니다.
- token 수에서 CLS 몇 개를 뺀 효과와, `N×N` patch-level attention topology를 바꾼 효과는 계산상 전혀 다르다.
- 번역에서 `global`만 보고 “전체를 본다/안 본다”고 쓰지 말고 무엇이 token이고 무엇이 connectivity인지 명시한다.

### DepthAnything backbone vs depth modality

- `DepthAnythingV2-Small backbone`은 pretrained RGB visual trunk의 출처일 수 있다.
- depth decoder가 실행되는지, depth map이 생성되는지, 그 depth tensor가 policy condition으로 소비되는지는 별도 사실이다.
- simulator ground-truth depth로 3D waypoint를 RGB pixel label에 project하는 offline pipeline과 runtime depth input을 분리한다.
- robot API에 `depth` field가 존재하는 것과 learned module이 그 tensor를 실제 소비하는 것도 분리한다.

### 재발 방지 modality table

| 단계 | RGB | Depth | Pose/3D | 산출물 |
|---|---|---|---|---|
| Offline label generation |  | privileged 가능 | trajectory/pose 가능 | pixel goal label |
| Training input |  |  |  | model tensor |
| Inference input |  |  |  | action/trajectory |
| Deployment plumbing | camera | sensor 존재 가능 | odometry 가능 | controller input |

빈칸을 추측으로 채우지 않는다. 코드에서는 argument 선언이 아니라 learned operation까지 dataflow를 추적한다.

## 3. 시간축의 정확한 의미를 보존한다

`anchor`, `current`, `history`, `streaming`은 쉽게 과해석된다.

DualVLN 사례에서 원문이 직접 말한 것은 System 2 마지막 RGB at `t`와 current RGB at `t+k`의 pair다. 이전 System-1 current frame의 누적, recurrent state, KV cache 유무는 source만으로 확정할 수 없다. 공개 implementation에서 확인했다면 구현 메모로만 둔다.

### 확인 질문

- Anchor는 언제 갱신되는가?
- Current frame은 매 tick 하나인가, sliding window인가?
- 이전 current feature가 다음 호출로 전달되는가?
- History는 raw image sequence인가, VLM latent에 간접 요약된 것인가?
- 학습 sample이 pair인가, temporal sequence인가?

## 4. 학습 단계와 optimizer 설정의 문단 경계를 보존한다

### 실패 사례

원문 부록은 다음을 별도 문단으로 썼다.

1. Stage 2에서 latent query와 diffusion policy를 train한다는 objective/module 설명
2. AdamW, learning rate, batch size, total steps

번역본이 두 문단을 하나로 합치면서 개념적 결론 직후 `AdamW optimizer...`가 튀어나와 문장이 부자연스러워졌다. 게다가 `고정 VLM까지 다시 훈련한다는 뜻이 아니다` 같은 번역자 해설이 source body에 섞였다.

### 권장 형식

```text
[학습 대상과 objective]
Stage 2에서는 ... 두 module을 공동 학습한다. Qwen2.5-VL은 고정되어 있고,
업데이트 대상은 두 module로 한정된다.

학습 설정. AdamW optimizer를 사용하며 initial learning rate는 ...이다.
Batch size는 ...이고, 총 ... step 학습한다.
```

### 규칙

- 원문의 paragraph break는 의미 경계로 간주하고 기본적으로 보존한다.
- objective/module/frozen parameter 설명과 optimizer hyperparameter를 한 문단으로 합치지 않는다.
- `end-to-end`의 범위는 실제 trainable parameter 목록과 함께 쓴다.
- “end-to-end = backbone까지 모두 finetune”이라고 자동 해석하지 않는다.
- 번역자 설명이 필요하면 본문이 아니라 대조 메모에 둔다.

## 5. Benchmark curation, training-data generation, metric을 분리한다

### Social-VLN 사례

한 인접 구간에 다음 세 가지가 함께 등장해 혼동되었다.

1. **Benchmark construction:** dynamic humanoid를 route 주변에 배치하고 완전 봉쇄 episode를 피함
2. **Evaluation:** NE/OS/SR/SPL과 HCR을 보고함
3. **Training data generation:** human mask trigger와 modified A*로 collision-free expert trajectory를 생성함

이 셋을 한 pipeline처럼 번역하면 평가 중 modified A*가 model을 돕는 것처럼 읽힐 수 있다.

### 주체 복원

`agent does not block the path entirely`처럼 `agent`가 여러 대상을 가리킬 수 있으면 반드시 실제 주체를 복원한다. 이 사례에서 길을 막지 않도록 검수한 대상은 navigation robot이 아니라 배치된 humanoid pedestrian이다.

### Metric 정의 부족

HCR이라는 이름과 표의 비율만으로 episode-level 공식, collision threshold, body-contact 판정을 만들어내지 않는다. 원문이 denominator와 event definition을 주지 않으면:

- 본문에는 저자가 직접 정의한 범위만 번역한다.
- 재현성 한계는 원문 대조 메모로 표시한다.
- “문맥상 자연스러운 해석”은 명시적으로 추정이라고 label한다.

## 6. 자연스러운 번역은 원문 paragraph를 지우는 일이 아니다

- `informative perspective`를 “정보성 높은 관점”이라고 직역하지 말고, 해당 문맥의 기능인 “목표를 판별하기에 적합한 시야”로 복원한다.
- `farthest successfully projected waypoint`는 거리만 멀다는 뜻이 아니라 current image에 projection이 성공한 future waypoint 집합 중 가장 먼 waypoint다.
- `view adjustment`는 명사구 하나로 두지 말고, 언제 turn action을 출력하고 언제 pixel goal을 출력하는지 조건을 풀어 쓴다.
- 다만 자연스럽게 풀어 쓰더라도 원문에 없는 causal claim·implementation detail·성능 평가를 추가하지 않는다.

### 의미 슬롯 검사

각 복합문에서 다음을 표로 복원한다.

- 주체
- 입력/관측
- 조건
- 선택 가능한 출력
- 반복/종료 조건
- 목적
- 학습 단계인지 평가 단계인지 runtime인지

## 7. HTML 2단 조판은 작은 heading split을 만든다

### 실제 실패

`table.wide`는 전체 폭이었지만 제목은 `<h3 class="section">`이었다. CSS가 다음과 같았다.

```css
.doc-title, h2.section { column-span: all; }
```

Chrome multicol print가 표 4 제목의 마지막 단어 `ablation`을 오른쪽 column으로 분리했다. 전체 contact sheet 축소본에서는 놓치기 쉬웠다.

### 수정

```css
.doc-title, h2.section, h3.section { column-span: all; }
table.wide { column-span: all; }
```

### 재발 방지

1. `h3.section` 수와 `table.wide` 수를 구조 assertion으로 센다.
2. `h3.section`을 포함하는 `column-span: all` selector가 있는지 static check한다.
3. wide table이 있는 모든 page를 120–150 dpi로 별도 rasterize한다.
4. 고해상도 PDF뿐 아니라 압축 delivery PDF도 같은 page를 다시 확인한다.
5. `validator PASS`를 시각 QA 대체물로 취급하지 않는다.

저장소의 `scripts/check_multicol_layout.py`를 HTML preflight에 사용한다.

## 8. 독립 fidelity audit가 필요하다

전면 재번역 agent가 문장을 자연스럽게 만들면서 code-derived interpretation을 body에 넣을 수 있다. DualVLN 3판에서는 독립 원문 충실도 감사에서 18개의 과강화·주체/단계 오류를 찾아 모두 교정했다.

### 2-pass review

- **Pass A — completeness:** source paragraph·figure·table·equation inventory와 번역 entity를 대조한다.
- **Pass B — fidelity:** 각 번역 문장에서 원문보다 강한 주장, code fact 혼입, 주체 변경, 단계 변경, 분모/threshold 창작을 찾는다.

동일한 agent가 번역과 감사를 모두 하면 자기 해석을 다시 정당화하기 쉽다. 가능하면 reviewer 역할을 분리한다. Reviewer 결과는 수정 대상의 exact fragment와 source 근거를 기록해야 한다.

## 9. PDF 수정 후 파생 산출물을 모두 다시 만든다

HTML 한 문장이나 CSS 한 줄을 고쳐도 다음을 전부 무효화한다.

- 고해상도 PDF
- 압축 delivery PDF
- validator output
- contact sheet 및 page-level screenshot
- SHA-256
- README의 파일 크기·hash
- Git LFS object

### 수정 후 고정 순서

```text
HTML patch
→ static structure assertion
→ high-resolution PDF render
→ validator
→ full contact sheet QA
→ affected pages 120–150 dpi QA
→ delivery PDF regenerate
→ delivery validator
→ affected delivery pages QA
→ SHA-256/README update
→ Git LFS status/commit/push/read-back
```

기존 PDF를 검증한 뒤 HTML만 고치거나, 고해상도 PDF만 재렌더하고 delivery PDF를 재사용하면 안 된다.

## 10. 사용자 제보를 reusable regression으로 바꾼다

사용자가 한 문장 또는 한 page를 지적하면 해당 위치만 고치고 끝내지 않는다.

- 같은 pattern을 문서 전체에서 검색한다.
- Stage 2 문단 문제라면 Stage 1의 동일한 optimizer 문단도 확인한다.
- 표 4 heading split이면 표 1–4를 모두 확인한다.
- 문제가 validator에 잡히지 않았다면 static assertion·script·skill rule 중 하나를 추가한다.
- 수정 이유, 재현 조건, verification evidence를 README/세션 기록에 남긴다.

## 최종 체크리스트

### Source fidelity

- [ ] source/code/analysis claim이 분리되어 있다.
- [ ] 초록의 개괄을 method tensor path로 강화하지 않았다.
- [ ] 공개 코드 사실은 `논문 본문 아님` 메모에만 있다.
- [ ] metric 정의가 없는데 공식·threshold를 만들지 않았다.

### VLA/VLN semantics

- [ ] explicit goal과 latent condition의 직접 입력 관계를 확인했다.
- [ ] CLS/global token과 global attention을 구분했다.
- [ ] anchor/current/history의 시간축과 누적 여부를 구분했다.
- [ ] backbone provenance와 runtime modality를 구분했다.
- [ ] offline label generation, training, evaluation, runtime을 분리했다.

### Korean prose

- [ ] 주체가 분명하다.
- [ ] objective 설명과 optimizer 설정이 별도 문단이다.
- [ ] 원문 paragraph break를 임의로 병합하지 않았다.
- [ ] 직역 명사구를 기능과 조건이 드러나는 문장으로 복원했다.

### Layout and release

- [ ] wide heading과 wide table이 같은 full-width context다.
- [ ] static multicol check가 PASS다.
- [ ] 전체 contact sheet와 affected-page 확대 QA가 PASS다.
- [ ] delivery PDF를 재생성·재검증했다.
- [ ] hash·README·LFS object가 최종 파일과 일치한다.
