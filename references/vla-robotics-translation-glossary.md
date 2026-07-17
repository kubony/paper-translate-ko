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

## Practical translation workflow

1. Before machine translating, protect glossary terms with placeholders so Google/DeepL-style translation does not over-translate them.
2. After translation, run a post-processing pass for known bad translations above.
3. Keep model names, benchmark names, dataset names, metric names, code flags, action dimensions, numeric values, and exact variable names unchanged.
4. Use paper-style declarative Korean (`~한다`, `~이다`), not polite endings.
5. For robotics papers with equations, convert LaTeX residue to readable monospace/Unicode approximations before rendering: e.g. `Xu = αu·X0 + σu·ε`, `L_flow = E[||Ẋu_hat - Ẋu||²₂]`.
6. Add 5–7 glossary decisions to the output PDF’s “번역 메모” block for terms that strongly affect interpretation.

## DualVLN-specific notes

- `DualVLN` is a dual-system VLN foundation model, not simply a VLA scaffold paper.
- Translate `Ground Slow, Move Fast` as a title in English, but explain as System 2가 천천히 grounding하고 System 1이 빠르게 trajectory를 생성하는 구조.
- `System 2`: VLM-based global planner; predicts mid-term waypoint / pixel goal via image-grounded reasoning.
- `System 1`: lightweight multimodal conditioning Diffusion Transformer policy; generates smooth trajectories in real time from explicit pixel goal + latent features.
