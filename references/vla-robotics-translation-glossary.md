# VLA/Robotics Korean Translation Glossary

Use this reference whenever translating AI robotics, VLA, VLN, embodied AI, robot foundation model, physical AI, autonomous driving, or related technical blogs/papers into Korean. User-corrected terminology in this glossary overrides generic machine-translation output and the broader style rules.

## High-priority user corrections

- `frontier model` → **프론티어 모델**. Never translate as “개척 모델”.
- `frontier AI` → **프론티어 AI**.
- `Physical AI` → **피지컬 AI**.
- `Vision-Language-Action`, `VLA` → first occurrence: **Vision-Language-Action(VLA, 비전-언어-액션)**; later: **VLA**.
- `foundation model` → **파운데이션 모델**. Avoid forcing “기반 모델/기초 모델”.
- `robot foundation model` → **로봇 파운데이션 모델**.
- `generalist policy` → **generalist policy** or **범용 로봇 policy**. Avoid “범형” unless quoting a source that uses it.
- `policy` → **policy**. Avoid over-translating as “정책” in robotics control/model contexts.
- `action` → **action**. Keep action-space/action-token/action-chunk terms in mixed notation.
- `embodiment` → **embodiment** or **로봇 몸체/몸체 형태**. Never “실체”.
- `embodied reasoning` → **embodied reasoning(체화 추론)** or **embodied reasoning**.
- `cross-embodiment` → **cross-embodiment**; optionally add “몸체 간” explanation on first use.
- `dexterous manipulation` → **dexterous manipulation** or **정교한 조작** depending on sentence flow; do not flatten to generic “조작” only.

## Keep these mostly in English

- Control/action terms: `direct control`, `code control`, `programmatic control`, `high-level control`, `low-level control`, `controller`, `policy`, `pretrained policy`, `gait policy`, `action`, `action space`, `action chunking`, `action tokenization`, `motor command`, `trajectory`.
- VLA architecture terms: `pixel goal`, `latent goal`, `latent queries`, `latent features`, `Diffusion Transformer`, `diffusion policy`, `flow matching`, `autoregressive`, `latent reasoning`, `test-time compute`, `Chain-of-Thought(CoT)`.
- Robotics/VLN terms: `locomotion`, `manipulation`, `dexterous manipulation`, `whole-body control`, `mobile manipulator`, `humanoid`, `quadruped`, `cross-embodiment`, `motion transfer`, `open-world generalization`, `grounding`, `spatial understanding`, `scene description`, `segmentation mask`, `depth map`, `depth heatmap`, `third-person camera`, `egocentric view`.
- Hardware/control terms: `backdrivable`, `tendon-driven`, `bi-directional actuation`, `retargeting`, `teleoperation`, `force sensing`, `tactile sensing`, `IPC`, `zero-copy`, `jitter`, `latency`, `observability`, `telemetry`.

## Known bad machine translations to correct

- `latency` → **latency / 지연 시간**, not “숨어 있음”.
- `locomotion` → **locomotion / 보행·이동**, not “기관차”.
- `quadruped` → **4족 보행 로봇 / quadruped**, not “네 발 달린 동물”.
- `autoregressive` → **autoregressive / 자기회귀**, not “자기 회기”.
- `grounding` → **grounding**, not “접지” unless explaining metaphorically.
- `embodiment` → **embodiment / 로봇 몸체**, not “실체”.
- `success rate` → **성공률**, not “성공 속도”.
- `retargeting` → **retargeting**, not “재표적화” unless giving a parenthetical explanation.
- `policy` → **policy**, not “정책” when it means learned robot controller/model behavior.
- `frontier` → **프론티어**, not “개척/최전방” in model/AI naming contexts.
- `noisy data`, `noisy dataset` → **노이지 데이터**, **노이지 데이터셋**, not “시끄러운 데이터/데이터셋”.
- `state space` → **상태 공간**, not “주 공간”.
- `train a model` → 모델을 **훈련한다**, not 모델을 “교육한다”.
- `hold/freeze the model fixed` → **모델 파라미터를 고정한다 / 업데이트하지 않는다**. 공간적 위치를 고정한다는 뜻으로 옮기지 않는다.
- `behavioral cloning (BC)` → 첫 등장에 **행동 복제(Behavioral Cloning, BC)** 또는 **behavioral cloning(BC)**; 이후 **BC**.
- `inverse dynamics model (IDM)` → 첫 등장에 **역동역학 모델(Inverse Dynamics Model, IDM)**; 이후 **IDM**.
- `action space` → **행동 공간**. `full`, `human`, `unmodified` 같은 수식 의미를 빠뜨리지 않는다.
- `out-of-distribution` → **학습 분포 밖(out-of-distribution)**, not “배포되지 않음”.
- `visual domain shift` → **시각적 domain shift / 시각적 도메인 차이**, not “시각적 영역의 영향력 있는 변화”.
- `different distribution of play` → **플레이 양상이 다름 / 플레이 행동 분포가 다름**.
- `nontrivial performance` → **무시할 수 없는 성능**, not “적지 않은 성능”.
- `craft a crafting table` → **제작대를 만들다**, not “제작대를 제작하다”.
- `go past this in the technology tree` → **기술 트리의 다음 단계로 나아가다**.
- `narrower datasets` → **범위가 더 좁은 데이터셋**, not “더 좁은 데이터셋”.
- defined data labels `clean` / `unclean` → **clean / unclean**; preserve the opposition and never assign the same translated label to both categories.
- `inventory` in game/UI contexts → **인벤토리**, not “재고”; `drag-and-drop inventory management` → **드래그 앤 드롭 방식의 인벤토리 관리**.
- academic `work` / `published work` → **연구** / **발표된 연구**, not “작업” / “출판된 작업”.
- `Sec. N`, `Section N` → **N절**. 문장 분리 전에 약어와 번호를 하나의 참조 단위로 보호한다.
- `contractor` in data collection → **인간 작업자(contractor)**. 계약 문서나 사업자 의미로 오해하지 않도록 실제 역할을 밝힌다.

## Sequential-model disambiguation

- `causal model`은 `casual model`과 다르다. 순차 모델 문맥에서는 보통 **미래 관찰을 참조하지 않는 모델**을 뜻한다.
- causal BC/policy는 현재 action을 결정할 때 `o_1, …, o_t`만 사용한다. 이를 일반적인 인과추론 모델로 풀어쓰지 않는다.
- non-causal IDM은 이미 녹화된 trajectory를 labeling하므로 `o_{t+1}` 같은 미래 관찰도 사용할 수 있다.
- `p_IDM(a_t | o_t, o_{t+1})`는 “두 화면이 주어졌을 때 그 사이에 수행된 action이 `a_t`일 확률”로 설명한다.
- 역할 차이는 한 문장으로 명시한다: **IDM은 앞뒤 영상을 보고 방금 수행된 action을 추정하고, BC는 현재까지의 화면만 보고 지금 수행할 action을 결정한다.**

## Practical translation workflow

1. Before machine translating, protect glossary terms with placeholders so Google/DeepL-style translation does not over-translate them.
2. After translation, run a post-processing pass for known bad translations above.
3. Keep model names, benchmark names, dataset names, metric names, code flags, action dimensions, numeric values, and exact variable names unchanged.
4. Use paper-style declarative Korean (`~한다`, `~이다`), not polite endings.
5. For robotics papers with equations, convert LaTeX residue to readable monospace/Unicode approximations before rendering: e.g. `Xu = αu·X0 + σu·ε`, `L_flow = E[||Ẋu_hat - Ẋu||²₂]`.
6. For conditional probabilities and sequential-model equations, add a short “수식 읽는 법” explanation that defines every symbol and distinguishes past/current/future observations.
7. Add 5–7 glossary decisions to the output PDF’s “번역 메모” block for terms that strongly affect interpretation.

## DualVLN-specific notes

- `DualVLN` is a dual-system VLN foundation model, not simply a VLA scaffold paper.
- Translate `Ground Slow, Move Fast` as a title in English, but explain as System 2가 천천히 grounding하고 System 1이 빠르게 trajectory를 생성하는 구조.
- `System 2`: VLM-based global planner; predicts mid-term waypoint / pixel goal via image-grounded reasoning.
- `System 1`: lightweight multimodal conditioning Diffusion Transformer policy; generates smooth trajectories in real time from explicit pixel goal + latent features.
- `self-directed view adjustment` → **자율적 시야 조정**. 모델이 camera 방향을 먼저 바꿀지, 현재 frame에서 pixel goal을 예측할지를 반복적으로 선택한다는 동작을 풀어 쓴다. 단순히 “view를 조절한다”로 두지 않는다.
- `informative perspective/viewpoint` → **목표 지점을 판별하기에 적합한 시야/관측 시점**. “정보성 높은 관점”, “까다로운 viewpoint를 처리한다” 같은 직역투를 금지한다.
- `history`가 RGB frame sequence를 뜻하면 **이전 관측 이력** 또는 **이전 RGB frame들**로 옮긴다. “history를 관측한다”라고 쓰지 않는다.
- `farthest pixel goal grounding`은 막연히 “가장 먼 Pixel Goal Grounding”으로 옮기지 않는다. DualVLN에서는 **현재 시야에서 확인 가능한 trajectory point 가운데 agent로부터 가장 먼 point를 pixel goal로 예측하는 방식**임을 제목 또는 첫 문장에서 풀어 쓴다.
- Visibility/depth 문장은 역할을 명시한다: `distance > depth value`인 trajectory point는 **다른 표면 뒤에 가려진 것으로 판정해 제외한다**. `visibility를 측정한다`, `occluded로 보고 제거한다`처럼 의미가 흐린 혼합문을 피한다.
- Backbone 명칭은 문서 전체에서 **Qwen2.5-VL**로 표준화하되, 원 논문이 사용한 모델 버전을 최신 Qwen 계열 모델로 임의 교체하지 않는다.
