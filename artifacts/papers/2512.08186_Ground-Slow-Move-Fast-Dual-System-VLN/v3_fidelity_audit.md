# `translation_v3.html` 원문 충실도 감사

- **감사 대상:** `/home/inkeun/tools/paper-translate-ko/artifacts/papers/2512.08186_Ground-Slow-Move-Fast-Dual-System-VLN/translation_v3.html`
- **대조 원문:** `source/sections/0_abstract.tex`–`7_appendix.tex`, `source/tables/*.tex`, `source/iclr2026_conference.tex`
- **범위:** 초록, 그림 설명, 서론, 관련 연구, 방법, Social-VLN, 실험, 결론, 기여·감사의 말, 부록 A–B, 표
- **판정 기준:** 원문보다 강한 단정, 원문에 없는 구현/코드 기반 해석, 번역자의 비평이 본문 번역에 섞인 경우, 행위 주체나 학습·평가·runtime 단계가 달라진 경우를 문제로 집계했다. 단순한 영문 혼합 표기나 자연스러운 의역은 집계하지 않았다.
- **총 문제 수:** **18개** (HIGH 4, MEDIUM 11, LOW 3)

## 요약

가장 큰 문제는 3.2절의 짧은 원문 설명(두 RGB를 **ViT encoder**로 처리하고, 두 시점 feature를 **self-attention**으로 fuse한 뒤, **Q-Former**로 32 token으로 압축한다)을 공개 구현에서 유추한 세부 동작처럼 확장해 본문 사실로 적은 것이다. 원문은 DINOv2의 CLS/global token 미사용, current-frame history 비누적, Q-Former의 learned-query/weighted-mixture 동작, 32 visual token과 32 waypoint의 비대응을 직접 진술하지 않는다. 또한 HCR 미정의 비평과 depth 사용 여부에 관한 구현 해석이 번역 본문에 들어가 있다.

`LoaderDrive`라는 문자열이나 LoaderDrive에 관한 해석은 대상 HTML에서 발견되지 않았다.

---

## 문제 목록

### 1. [HIGH] 초록의 개괄 표현을 System 1의 직접 입력 명세로 단정

- **위치:** 표지 뒤 `번역 메모` 두 번째 항목
- **정확한 기존 문구:** “**System 2는 실행 시 명시적 pixel goal과 latent goal을 만들고, System 1은 이 두 조건 및 최신 시각 조건을 받아 trajectory를 생성한다.** 직접 System 1, pixel-goal-only 변형, latent 제거 변형을 서로 혼동하지 않는다.”
- **근거 원문:** 초록은 “System~1 … **leveraging both explicit pixel goals and latent features from System~2**”라고 개괄한다(`0_abstract.tex:10`). 그러나 방법의 직접 조건 명세는 “two conditioning signals (**trajectory latents $Z'$ and fused RGB tokens $F$**)” 및 `f_θ(X_u, u, Z' ⊕ F)`이다(`3_method.tex:34, 40–44`). 부록 코드도 `DiT(x, timestep, pixel_goal_latents)`만 보이며(`7_appendix.tex:100–105`), explicit pixel coordinate가 별도 tensor로 직접 투입된다고 쓰지 않는다.
- **문제:** 초록의 기능적 설명과 방법 수식/호출 경로를 구분하지 않고, explicit pixel goal 자체가 System 1의 별도 직접 condition이라고 확정한다.
- **권장 수정문:** “초록은 System 1이 explicit pixel goal과 System 2의 latent feature를 활용한다고 개괄한다. 방법 수식은 System 1의 직접 조건을 `Z′`와 fused RGB token `F`로 표기하므로, pixel-goal 정보가 `Z′`의 context를 통해 전달되는 설명과 별도 직접 입력을 구분해야 한다.”

### 2. [MEDIUM] 두 RGB의 비누적 history와 Q-Former 내부 동작을 원문 사실로 제시

- **위치:** `번역 메모` 세 번째 항목
- **정확한 기존 문구:** “System 1의 두 RGB 시점은 System 2가 계획할 때 본 **plan-anchor RGB**와 해당 fast-policy tick의 **current RGB**이다. **current frame을 누적 history로 해석하지 않는다. 두 시점의 patch token은 self-attention으로 결합되고, Q-Former의 32개 learned query가 결합 memory를 32개의 새 요약 token으로 합성한다.**”
- **근거 원문:** “System~1 encodes both the RGB features corresponding to the last frame from System~2 at time $t$ and the current observation at time $t+k$. Both images are first processed by a **ViT encoder** … fused … using a **self-attention module** … compressed using a **Q-Former into a compact set of 32 tokens**”(`3_method.tex:29–31`).
- **문제:** 원문은 두 frame을 말하지만 history가 절대로 누적되지 않는다고 명시하지 않는다. 또한 patch token, 32 learned query, memory에서 새 token을 합성한다는 내부 메커니즘도 직접 진술하지 않는다.
- **권장 수정문:** “System 1은 time $t$의 System 2 마지막 frame과 time $t+k$의 현재 관측을 ViT로 encode하고, 두 시점 feature를 self-attention으로 fuse한 뒤 Q-Former로 32 token으로 압축한다.” 구현 확인 내용은 별도의 **‘번역·구현 대조 메모’** 상자로 옮기고 논문 직접 진술이 아님을 표시한다.

### 3. [HIGH] DepthAnythingV2-Small을 DINOv2 visual trunk로 특정하고 depth 미사용을 확정

- **위치:** `번역 메모` 네 번째 항목
- **정확한 기존 문구:** “**DepthAnythingV2-Small은 System 1의 RGB encoder에 쓰이는 DINOv2 visual trunk를 가리킨다.** 이는 학습 label 생성 시 쓰는 depth map이나 현실 실행 시 전송하는 RGB-D, **depth decoder를 System 1이 직접 조건으로 사용한다는 뜻이 아니다.**”
- **근거 원문:** 구현 절은 “The RGB encoder is implemented using the **ViT backbone of DepthAnythingV2-Small**”이라고만 한다(`3_method.tex:54`). 관련 연구는 System 1을 “an **RGB-only visual navigation policy**”라고 부른다(`2_related_work.tex:11`). 현실 실험은 robot이 “synchronized **RGB-D images**”를 server로 보낸다고 한다(`5_experiments.tex:51–53`).
- **문제:** DINOv2 trunk라는 구체화와 depth decoder의 호출/미호출은 원문 문장에 없다. 서로 다른 원문 문장을 조합해 공개 구현의 call path를 사실로 확정한다.
- **권장 수정문:** “원문은 System 1의 RGB encoder를 DepthAnythingV2-Small의 ViT backbone으로 구현했다고 설명하며, 관련 연구 절에서는 System 1을 RGB-only policy라고 부른다.” DINOv2/depth-decoder call path는 구현 대조 메모로만 제시한다.

### 4. [LOW] HCR 정의 부재에 관한 편집자 비평이 일반 번역 메모에 사실처럼 들어감

- **위치:** `번역 메모` 다섯 번째 항목
- **정확한 기존 문구:** “**원문이 HCR 집계식을 정의하지 않으므로 임의 공식을 덧붙이지 않는다.**”
- **근거 원문:** 원문은 “introduce a **Human Collision Rate (HCR)** metric to explicitly quantify failures…”라고만 쓴다(`4_benchmark.tex:23`).
- **문제:** 관찰 자체는 맞지만 논문 내용의 번역이 아니라 번역자의 원문 비평이다. 현재 제목은 단순 `번역 메모`이며 원문/구현 대조와 편집자 주석의 경계가 불분명하다.
- **권장 수정문:** 본문 번역에서는 삭제한다. 꼭 보존하려면 별도 상자를 **“번역·원문 대조 메모(논문 본문 아님)”**로 명시하고 “원문 제공 범위에서는 HCR 산식이 제시되지 않는다”라고 적는다.

### 5. [MEDIUM] System 2가 두 작업을 엄격히 ‘번갈아’ 수행한다고 강화

- **위치:** 3.1절 첫 문장
- **정확한 기존 문구:** “System 2는 고수준 pixel-goal grounding과 자율적 시야 조정을 **반복적으로 번갈아 수행한다.**”
- **근거 원문:** “System~2 **integrates** high-level pixel-goal grounding with self-directed view adjustment **in a iterative process**” 및 매 step에서 view를 조정할지 pixel goal을 출력할지 결정한다고 한다(`3_method.tex:10–11`).
- **문제:** iterative integration/선택을 엄격한 교대(alternation) 순서로 강화한다. 연속 turn action은 최대 네 개까지 출력할 수 있어(`7_appendix.tex:28–35`) 실제로도 단순 교대라고 단정하기 어렵다.
- **권장 수정문:** “System 2는 고수준 pixel-goal grounding과 자율적 시야 조정을 반복적 과정으로 통합한다.”

### 6. [LOW] 가시성용 depth를 ‘offline label filtering’ 및 runtime 비조건으로 해설

- **위치:** 3.1절 `현재 시야에서 확인 가능한 최원거리 Pixel Goal Grounding` 문단 끝
- **정확한 기존 문구:** “**여기서 depth는 offline label filtering에 쓰이며 System 1의 runtime depth condition을 뜻하지 않는다.**”
- **근거 원문:** 해당 문단은 training sample 생성 때 depth map과 camera–point distance로 occlusion을 판정한다고 한다(`3_method.tex:13–14`). 이 자리에서 System 1 runtime 입력이나 depth decoder를 논하지 않는다.
- **문제:** label 생성 단계라는 해석은 문맥상 타당하지만, System 1 runtime condition에 관한 부정은 해당 원문에 없는 교차 절 해설이다.
- **권장 수정문:** “이 depth map은 pixel-goal grounding 학습 sample을 생성할 때 point의 가시성을 판정하는 데 사용된다.” runtime 입력에 관한 해석은 구현 대조 메모로 옮긴다.

### 7. [MEDIUM] current RGB history가 비누적이라고 본문에서 확정

- **위치:** 3.2절 `Multi-Modal Conditioning Diffusion Transformer` 세 번째 문단
- **정확한 기존 문구:** “**이 입력은 누적된 current-frame history가 아니라 매 호출마다 사용하는 고정 anchor와 해당 tick의 최신 frame 두 장이다.**”
- **근거 원문:** 원문은 time $t$의 System 2 마지막 frame과 time $t+k$의 current observation을 encode한다고만 한다(`3_method.tex:29–31`). System 2 자체는 current RGB와 history를 본다(`3_method.tex:11`).
- **문제:** System 1 입력에 두 시점이 포함된다는 것과 history buffer가 구현상 존재하지 않는다는 것은 다른 주장이다. 후자는 원문 직접 진술이 아니다.
- **권장 수정문:** “System 1은 time $t$에 System 2가 사용한 마지막 RGB frame과 time $t+k$의 현재 관측을 encode한다.”

### 8. [HIGH] DINOv2 patch token 및 CLS/global/depth-decoder 미사용을 방법 본문으로 삽입

- **위치:** 3.2절 같은 문단
- **정확한 기존 문구:** “**두 image는 DepthAnythingV2-Small의 DINOv2 visual trunk에서 patch feature로 변환되며, CLS/global token이나 depth decoder 출력은 이 설명의 조건에 포함되지 않는다.**”
- **근거 원문:** 방법 3.2절은 “Both images are first processed by a **ViT encoder to extract high-dimensional visual features**”라고만 한다(`3_method.tex:31`). DepthAnythingV2-Small은 뒤의 구현 세부사항에서 ViT backbone으로만 명명된다(`3_method.tex:54`).
- **문제:** encoder 정체, token 선택, decoder call path를 공개 구현 수준으로 구체화했다. 특히 CLS/global token 미사용은 원문에 전혀 없다.
- **권장 수정문:** “두 image는 먼저 ViT encoder로 처리되어 고차원 visual feature로 변환된다.” 나머지는 출처와 검증 시점을 붙인 구현 대조 메모로만 둔다.

### 9. [MEDIUM] self-attention이 변화량과 camera 관계를 반영한다고 기능을 추가

- **위치:** 3.2절 같은 문단
- **정확한 기존 문구:** “이어 self-attention module이 anchor와 current의 patch token을 서로 참조하게 하여 **두 시점의 변화와 camera 관계가 반영된 fused memory를 만든다.**”
- **근거 원문:** “These features are then **fused across the two time steps using a self-attention module**”(`3_method.tex:31`).
- **문제:** 원문은 두 시점 feature의 fusion만 말한다. 변화량 추정, camera 관계 표현, `memory`라는 해석은 원문에 없다.
- **권장 수정문:** “두 시점의 feature는 self-attention module로 결합된다.”

### 10. [HIGH] Q-Former를 32 learned query의 weighted mixture 합성기로 단정

- **위치:** 3.2절 같은 문단
- **정확한 기존 문구:** “**Q-Former의 32개 learned query는 이 memory 전체를 cross-attention하여 weighted mixture로 32개의 새 요약 token을 합성한다.**”
- **근거 원문:** “the fused features are further **compressed using a Q-Former into a compact set of 32 tokens**”(`3_method.tex:31`).
- **문제:** learned query의 수, cross-attention 범위, weighted mixture, 새 token 합성은 Q-Former에 대한 일반 지식이나 구현에서 유추한 설명이며 논문 직접 진술이 아니다.
- **권장 수정문:** “결합된 feature는 Q-Former를 통해 compact한 32개 token으로 압축된다.”

### 11. [MEDIUM] 32 visual token과 32-step trajectory의 비대응을 원문 사실로 단정

- **위치:** 3.2절 같은 문단 마지막 문장
- **정확한 기존 문구:** “**이 32개 visual token은 DiT의 빠른 갱신 visual condition이며, 32-step trajectory horizon과 일대일로 대응하지 않는다.**”
- **근거 원문:** 원문은 trajectory가 “32 dense waypoints”라고 하고(`3_method.tex:28`), 별도로 Q-Former가 “a compact set of 32 tokens”을 만든다고 한다(`3_method.tex:31`). 두 수의 대응 여부는 설명하지 않는다.
- **문제:** 비대응이 아키텍처상 그럴듯하더라도 원문에 없는 부정 명제다.
- **권장 수정문:** “Q-Former가 만든 32개 token은 DiT의 high-frequency visual condition으로 사용된다.” 대응 여부는 단정하지 않거나 구현 대조 메모에서만 언급한다.

### 12. [MEDIUM] 구현 세부사항에서 DINOv2와 depth-decoder 해석을 다시 본문에 삽입

- **위치:** 3.3절
- **정확한 기존 문구:** “System 1의 RGB encoder는 **DepthAnythingV2-Small에 포함된 DINOv2 ViT visual trunk**로 구현하며, **이 문장은 depth decoder나 depth map을 System 1 condition으로 사용한다는 뜻이 아니다.**”
- **근거 원문:** “The RGB encoder is implemented using the **ViT backbone of DepthAnythingV2-Small**”(`3_method.tex:54`).
- **문제:** `DINOv2` 특정과 decoder/map 미사용 해설 모두 원문 문구를 넘어선다.
- **권장 수정문:** “System 1의 RGB encoder는 DepthAnythingV2-Small의 ViT backbone으로 구현한다.”

### 13. [MEDIUM] 그림에서 interaction 유형 목록과 ‘scenario inventory’ 지위를 창작

- **위치:** 4절 `Benchmark 구축` 두 번째 문단
- **정확한 기존 문구:** “**그림 3은 정면 접근, 통과할 틈을 기다리는 상황, 양보, 여러 humanoid와의 동시 조우, 교차 지점 조우 등 Social-VLN이 다루는 정성적 interaction 유형을 보여 준다. 각 유형은 별도의 metric이 아니라 socially-aware obstacle avoidance를 폭넓게 시험하기 위한 scenario inventory이다.**”
- **근거 원문:** 본문은 “Social-VLN enables a comprehensive assessment … **in diverse situations, as shown in Figure 3**”이라고만 하고(`4_benchmark.tex:19–20`), 그림 설명도 single/multiple humanoid 상황을 말할 뿐이다(`4_benchmark.tex:3–7`).
- **문제:** 정면 접근·대기·양보·교차 지점이라는 유형명과 각 유형이 별도 metric이 아니라는 분류는 active LaTeX 원문에 없다.
- **권장 수정문:** “그림 3은 단일 또는 여러 humanoid가 등장하는 다양한 robot–humanoid interaction 상황을 보여 준다.”

### 14. [MEDIUM] episode 검수 목적을 ‘영구 봉쇄/해결 불가능한 폐색’으로 강화

- **위치:** 4절 같은 문단
- **정확한 기존 문구:** “배치된 humanoid가 통로를 **영구적으로 완전히 봉쇄하지 않는지** episode별로 확인하여, 실패가 **해결 불가능한 물리적 폐색만** 반영하지 않게 한다.”
- **근거 원문:** “verify each episode to ensure agents **do not block the path entirely**, so that failures don't reflect just **simple physical obstructions**”(`4_benchmark.tex:21`).
- **문제:** `영구적으로`, `해결 불가능한`은 원문보다 강한 조건이다. 원문은 path를 완전히 막지 않는지 확인한다고만 한다.
- **권장 수정문:** “각 episode에서 agent가 경로를 완전히 막지 않는지 확인하여, 실패가 단순한 물리적 방해만을 반영하지 않게 한다.”

### 15. [MEDIUM] HCR 미정의 비평을 Social-VLN 본문 번역에 삽입

- **위치:** 4절 같은 문단
- **정확한 기존 문구:** “**다만 원문은 HCR의 분모, contact threshold, episode/step 단위 집계식을 정의하지 않으므로 여기서 임의의 공식을 확정하지 않는다.**”
- **근거 원문:** “we further introduce a **Human Collision Rate (HCR)** metric to explicitly quantify failures caused by unsafe interactions with dynamic pedestrians”(`4_benchmark.tex:23`).
- **문제:** 분모/contact threshold/집계 단위가 없다는 것은 번역자의 critique이며, 원문 저자의 본문 진술처럼 같은 문단에 섞여 있다.
- **권장 수정문:** 본문은 “표준 VLN metric에 더해 dynamic pedestrian과의 unsafe interaction으로 인한 실패를 수량화하는 Human Collision Rate(HCR)를 도입한다.”에서 끝낸다. 정의 부재는 별도의 **‘번역·원문 대조 메모(논문 본문 아님)’**에 둔다.

### 16. [MEDIUM] 현실 RGB-D 전송과 System 1 depth-decoder 미사용을 연결해 확정

- **위치:** 5.2절 `실험 설정`
- **정확한 기존 문구:** “**여기서 RGB-D 전송은 배치 pipeline의 센서 구성이고, 3.3절에서 설명한 System 1 visual encoder가 depth decoder 출력을 조건으로 쓴다는 뜻은 아니다.**”
- **근거 원문:** 현실 실험은 “robot streams synchronized **RGB-D images** to a remote server”라고 한다(`5_experiments.tex:51–52`). 방법은 RGB encoder가 DepthAnythingV2-Small의 ViT backbone이라고만 한다(`3_method.tex:54`).
- **문제:** 두 문장을 구분하려는 주석은 유용하지만, depth decoder 호출 여부는 원문이 직접 설명하지 않은 구현 해석이다.
- **권장 수정문:** 본문에는 “Runtime에는 robot이 동기화된 RGB-D image를 remote server로 전송하고 dual-system model이 비동기 inference를 수행한다.”만 남긴다. 센서 stream과 model condition의 차이는 구현 대조 메모로 옮긴다.

### 17. [LOW] 원문의 ‘32 trajectories’를 ‘32개 후보’로 변경

- **위치:** 5.2절 `실험 설정`
- **정확한 기존 문구:** “System 1은 TensorRT로 0.03초 안에 **32개의 trajectory 후보를 병렬 생성한다.**”
- **근거 원문:** “System~1 **generates 32 trajectories in parallel** within 0.03s using TensorRT”(`5_experiments.tex:53`).
- **문제:** `후보`는 32개 중 하나를 선택하는 후속 selection/ranking 단계를 암시하지만 원문은 후보나 선택 절차를 말하지 않는다. 한편 방법 절의 출력은 32 dense waypoint로 된 trajectory이므로 숫자 32가 서로 다른 의미로 쓰일 가능성도 있어 원문 이상으로 해석하면 안 된다.
- **권장 수정문:** “System 1은 TensorRT를 사용해 0.03초 안에 32개 trajectory를 병렬로 생성한다.” 원문의 모호성은 그대로 보존한다.

### 18. [MEDIUM] attention weight에 관한 올바르지만 원문에 없는 해석상 경고 삽입

- **위치:** 부록 B 마지막 문장
- **정확한 기존 문구:** “**다만 attention weight는 token 간 mixing weight이며, 그 자체를 물체 존재 확률이나 인과적 중요도로 간주해서는 안 된다.**”
- **근거 원문:** 부록은 deepest layer가 STOP token에 큰 attention weight를 주며, 저자들은 이를 visual/language cue를 통합해 task completion을 판단한다는 근거로 해석한다(`7_appendix.tex:135–141`). attention의 비인과성에 관한 경고는 없다.
- **문제:** 과잉해석을 막는 일반적으로 타당한 주의지만 저자의 진술이 아니며, 번역 본문에 삽입되어 원문 해석의 일부처럼 보인다.
- **권장 수정문:** 본문에서는 해당 문장을 삭제한다. 보존하려면 “번역자 주: …”로 명시한 별도 메모 상자에 둔다.

---

## 섹션별 최종 판정

| 구간 | 판정 | 비고 |
|---|---|---|
| 초록·그림 1 | 본문 번역은 대체로 충실 | 번역 메모가 explicit pixel goal의 직접 conditioning을 과도하게 확정함 |
| 서론·관련 연구 | 충실 | 집계할 수준의 주체/단계 오류 없음 |
| 방법 3.1 | 수정 필요 | 엄격한 교대 표현, runtime depth 해설 추가 |
| 방법 3.2–3.3 | 중대한 수정 필요 | 공개 구현/architecture 관행에서 유추한 DINOv2·token·Q-Former 세부사항 다수 |
| Social-VLN | 수정 필요 | 원문에 없는 scenario 목록, HCR critique, 봉쇄 조건 강화 |
| Simulation 실험 | 충실 | 표 수치와 metric 설명에서 별도 문제 없음 |
| 현실 실험 | 수정 필요 | depth-decoder 해석 및 `후보` 의미 추가 |
| Ablation·결론·감사의 말 | 충실 | 원문의 저자 해석 범위 내 |
| 부록 A | 충실 | Stage 1/2 주체와 frozen QwenVL 설명은 원문에 근거함 |
| 부록 B | 수정 필요 | attention 해석 경고는 번역자 주석으로 분리해야 함 |
| 표 1–4 | 충실 | 수치·행/열·표제에서 추가 fidelity 문제를 찾지 못함 |

## 권고 원칙

1. 번역 본문에는 active LaTeX 원문이 직접 말한 수준만 남긴다.
2. 공개 코드나 model package에서 확인한 call path는 별도 **“번역·구현 대조 메모(논문 본문 아님)”** 상자에 출처와 commit/version을 붙여 기록한다.
3. 초록의 “explicit pixel goals and latent features를 활용”한다는 기능적 개괄과, 방법 수식의 직접 condition `Z′ ⊕ F`를 함께 보존하되 어느 한쪽으로 과잉 통합하지 않는다.
4. 논문이 정의하지 않은 HCR 산식, token 대응 관계, history buffer 부재, depth decoder 호출 여부는 본문에서 긍정·부정 어느 쪽으로도 확정하지 않는다.

---

## 수정 반영 결과

아래 18개 항목은 `translation_v3.html`에 모두 반영했다. 논문이 직접 서술하지 않은 공개 구현 해석은 본문에서 제거하고, 보존할 구현 확인 내용은 범위와 기준일을 명시한 `번역·구현 대조 메모(논문 본문 아님)` 상자로 분리했다.

| 번호 | 상태 | 반영 내용 |
|---:|:---:|---|
| 1 | **RESOLVED** | 초록의 기능적 개괄과 방법 수식의 직접 condition `Z′ ⊕ F`를 구현 대조 메모에서 구분했다. |
| 2 | **RESOLVED** | 본문은 두 시점·ViT·self-attention·Q-Former 32 token이라는 원문 직접 서술만 남겼다. |
| 3 | **RESOLVED** | DINOv2/depth call-path 단정을 본문에서 제거하고 구현 대조 메모로 분리했다. |
| 4 | **RESOLVED** | 일반 번역 메모의 HCR 비평을 삭제하고 논문 본문 아님이 명시된 별도 상자로 옮겼다. |
| 5 | **RESOLVED** | `반복적으로 번갈아 수행한다`를 `반복적 과정으로 통합한다`로 수정했다. |
| 6 | **RESOLVED** | 해당 depth map의 역할을 pixel-goal grounding 학습 sample 가시성 판정으로만 기술했다. |
| 7 | **RESOLVED** | current history 비누적 단정을 본문에서 제거했다. |
| 8 | **RESOLVED** | DINOv2 patch/CLS/global/depth-decoder 세부사항을 방법 본문에서 제거했다. |
| 9 | **RESOLVED** | 변화량·camera 관계·memory 해석을 삭제하고 self-attention 결합만 남겼다. |
| 10 | **RESOLVED** | learned query/cross-attention/weighted mixture 단정을 삭제하고 Q-Former의 32 token 압축만 남겼다. |
| 11 | **RESOLVED** | 32 visual token과 32 waypoint의 비대응 단정을 본문에서 제거했다. |
| 12 | **RESOLVED** | 3.3절을 `DepthAnythingV2-Small의 ViT backbone`이라는 원문 수준으로 수정했다. |
| 13 | **RESOLVED** | 창작된 interaction 유형과 scenario inventory 설명을 삭제했다. |
| 14 | **RESOLVED** | `영구적`·`해결 불가능한`이라는 강화 표현을 원문 수준으로 완화했다. |
| 15 | **RESOLVED** | HCR 정의 부재 비평을 본문과 분리된 원문 대조 메모 상자로 옮겼다. |
| 16 | **RESOLVED** | 현실 RGB-D stream과 depth-decoder 조건 여부를 연결한 본문 해설을 제거했다. |
| 17 | **RESOLVED** | `32개의 trajectory 후보`를 원문대로 `32개 trajectory`로 수정했다. |
| 18 | **RESOLVED** | 원문에 없는 attention weight 경고를 번역 본문에서 삭제했다. |

**최종 상태: 18/18 RESOLVED.**
