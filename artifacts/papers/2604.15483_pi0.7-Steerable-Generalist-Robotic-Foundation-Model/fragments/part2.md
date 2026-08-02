# 6. π0.7 모델과 학습 레시피

**P2-001 (source lines 341–345)**  
이제 다양한 데이터로 학습하여 π0.7 모델에 서로 다른 context를 통합하는 방법과 모델 아키텍처, 학습 및 추론의 세부 사항을 논의한다.

## 6.1 학습 데이터셋

**P2-002 (source lines 348–352)**  
π0.7의 학습 데이터셋은 다양한 환경에서 여러 로봇 플랫폼(고정형과 이동형, 단일 팔과 양팔 모두)을 사용해 폭넓은 작업을 수행한 시연 데이터로 구성된다. 환경에는 사내의 실험실형 및 가정형 환경과 실제 가정 환경이 포함된다. 이 밖에도 대규모 policy 평가에서 얻은 자율 데이터, policy rollout 중 인간이 개입한 데이터, 오픈 소스 로봇 데이터셋, 1인칭 인간 비디오 데이터, 그리고 객체 위치 추정 및 속성 예측, 시각 질의응답, 텍스트 전용 예측을 포함한 웹의 보조 비로봇 데이터 소스를 사용한다. 사내 로봇 데이터와 웹 비디오의 비디오 캡셔닝을 비롯한 비디오-언어 작업도 포함한다.

**P2-003 (source line 354)**  
고전적인 Vision-Language-Action(VLA, 비전-언어-액션) 학습 파이프라인에서 크게 벗어나, 학습에 준최적 로봇 데이터를 광범위하게 활용한다. 여기에는 품질이 낮은 시연(실패 episode 또는 상당히 많은 실수가 포함된 성공 episode)과 모델 평가 실험 중 이전 버전 모델이 수집한 데이터가 모두 포함된다. 단, 일반화에 초점을 둔 평가 작업에서 수집된 자율 데이터는 모두 학습에서 제외하며, 여기에는 7절의 작업도 포함된다. 예를 들어 RL 학습 중 π*₀.₆ 모델이 수집한 데이터를 추가 예시로 사용함으로써, π0.7이 사실상 그 행동을 distillation할 수 있게 한다. episode metadata를 context에 통합하면 모델이 이 모든 평가 데이터를 효과적으로 사용할 수 있으며, 7.1절에서 보이듯 RL로 개별 작업의 고성능에 특화된 모델과 비슷한 성능을 달성할 수 있다. 이는 범용 π0.7 모델이 RL로 학습된 specialist의 역량을 물려받는 일종의 “distillation” 과정에 해당한다. 준최적 데이터는 특정 작업에서 가능한 상태와 시나리오도 다양화하고 견고성을 강화하여, 고도의 기민성이 필요한 작업에서는 때때로 RL 학습 policy 또는 일반적으로 단일 작업에 post-training된 policy보다도 높은 성능을 내게 한다.

## 6.2 모델 아키텍처

**P2-004 (source lines 357–360)**  
이전 π₀.₅ 및 π₀.₆ 모델과 비교할 때 π0.7의 주요 아키텍처 변경점은 `MEM`의 history vision encoder를 사용하고 visual subgoal 이미지를 context에 포함한다는 것이다.

**P2-005 (source lines 361–363)**  
모델은 최대 네 개의 카메라 이미지(정면 view, 손목 view 두 개, 선택적인 후면 view)를 입력으로 받으며, 각 이미지에는 최대 여섯 개의 history frame이 포함된다. 또한 후면 view를 제외한 최대 세 개의 subgoal 이미지를 입력으로 받는다. history frame은 vision encoder를 거쳐 단일 frame과 같은 수의 token으로 압축되며, subgoal 이미지도 동일한 encoder로 처리된다. 카메라 observation과 subgoal 이미지는 모두 먼저 448×448 pixel로 크기를 조정한다. history frame은 1초 stride로 샘플링하며, 전체 history frame은 확률 0.3으로 전부 dropout한다. 후면 view 이미지도 사용 가능한 경우 확률 0.3으로 dropout한다.

**P2-006 (source lines 365–366)**  
block-causal masking 방식을 사용한다. observation token과 subgoal image token은 각각의 내부에서 bidirectional attention을 사용하고, goal-image token은 observation에도 추가로 attention할 수 있다. 그 뒤의 text token은 causal attention을 사용한다(appendix의 attention mask 시각화 참조). 로봇의 proprioceptive state **q**ₜ(history state 포함)도 model backbone에 입력한다. **q**ₜ를 표현하기 위해 discretized text token을 사용하는 π₀.₆과 달리, π0.7은 `MEM`을 따라 state 차원을 backbone 차원으로 매핑하는 linear projection으로 state를 embedding한다. 각 history state는 개별 token으로 취급하며, history frame이 dropout되면 대응하는 state token도 masking한다.

**P2-007 (source line 368)**  
더 경량인 “action expert”는 flow matching objective로 continuous action을 예측하도록 학습되는 860M-parameter transformer이다. flow matching의 timestep 정보를 주입하기 위해 adaptive RMSNorm을 사용한다. action expert가 처리하는 action token 수는 50개로 고정되며, 이는 50 step의 action chunk를 나타낸다. 50개 token은 서로 bidirectional attention을 수행하며 VLM backbone activation에도 attention할 수 있다.

**P2-008 (source line 370)**  
π0.7은 추론 지연이 있을 때 매끄러운 action trajectory를 생성하기 위해 real-time action chunking(RTC)의 학습 시점 버전도 사용한다. 학습 중에는 0~12 timestep의 지연을 시뮬레이션하며, 이는 50Hz 로봇에서 최대 240ms의 추론 latency에 해당한다.

## 6.3 Subgoal 이미지를 사용한 학습

**P2-009 (source lines 372–374)**  
π0.7이 subgoal 이미지를 처리하도록 학습할 때는 서로 다른 지연과 서로 다른 이미지 품질을 가진 goal을 수용해야 하며, 여기에는 world model이 생성한 이미지도 포함된다. 따라서 학습 중 모델에 context로 제공할 subgoal을 신중하게 선택해야 한다. 학습 trajectory의 미래 timestep에서 얻은 실제 이미지와 생성 이미지를 조합하여 학습한다. 실제 이미지의 timestep을 선택할 때는 다음 샘플링 방식이 효과적이었다. 확률 0.25로 segment 종료 이미지를 샘플링하며, 이는 world model의 prediction target과 일치한다. 확률 0.75로는 현재 timestep에서 0~4초 뒤의 미래 이미지를 균등하게 샘플링한다. 이러한 실제 이미지에 더해, 실제 이미지와 생성 이미지 사이의 train-test 불일치를 완화하기 위해 world model에서 다수의 subgoal 이미지를 샘플링하고, 실제 미래 이미지 대신 이 *생성* 이미지를 π0.7의 context에 추가한 별도의 학습 예시를 구성한다.

# 7. Runtime에서 π0.7 prompting

**P2-010 (source lines 383–386)**  
runtime에는 어떠한 작업별 post-training도 하지 않고, 원하는 행동에 따라 서로 다른 형태의 context로 π0.7을 구성한다. 모든 작업에서 항상 control mode와 episode metadata를 모델 prompt에 제공한다.

**P2-011 (source lines 387–392)**  
episode metadata는 다음과 같이 선택한다.

- 전체 속도: 작업의 episode length에 대한 15th percentile로 작업별 설정한다.
- 전체 품질: 최고 점수인 5로 항상 설정한다.
- 실수: 실수가 없다는 의미의 false로 항상 설정한다.

**P2-012 (source lines 393–394)**  
subtask instruction **rawtext**ₜ는 학습된 high-level language policy 또는 coaching을 수행하는 인간 감독자가 제공한다(7.4절 참조). subgoal 이미지를 사용할 때는 semantic intent가 바뀌는 경우, 즉 새로운 **rawtext**ₜ가 주어지는 경우와 마지막 subgoal 이미지가 생성된 뒤 Δ=4초가 지난 경우 중 먼저 발생하는 시점에 subgoal 이미지를 갱신한다. 전체 workflow는 Algorithm 1에 제시한다. 비동기 추론을 적용하여 visual subgoal 생성과 subtask instruction 생성을 별도 thread에서 수행하며, VLA 추론은 항상 현재 사용 가능한 최신 결과를 사용한다.

**P2-013 (source lines 396–403)**  
모든 실험에서 50-step action chunk를 생성하는 데 denoising step 5회를 사용하고, chunk에서 Ĥ ∈ {15, 25} step을 실행한다. 각 prompt component를 dropout과 함께 학습하므로, π0.7은 prompt의 어느 부분에든 classifier-free guidance(CFG)를 사용할 수 있다. 예를 들어 생성 action을 더 높은 속도 쪽으로 유도할 수 있다. 구체적으로 각 action denoising step은 다음을 따른다.

EQUATION 1:
```text
∇ₐ log πθ(aₜ:ₜ₊H | oₜ, Cₜ)
+ β[∇ₐ log πθ(aₜ:ₜ₊H | oₜ, Cₜ)
    − ∇ₐ log πθ(aₜ:ₜ₊H | oₜ, Cₜᵘⁿᶜᵒⁿᵈ)]
```

여기서 Cₜᵘⁿᶜᵒⁿᵈ는 “unconditional” mode에서 사용하는 context 집합이고 β는 CFG weight이다. context의 어느 부분이든 dropout할 수 있지만, 고도의 기민성이 필요한 작업에서 강한 성능을 끌어내기 위해 episode metadata에 CFG를 적용한다. β ∈ {1.3, 1.7, 2.2}의 중간 정도 값을 사용한다.

**P2-014 (source lines 405–425)**  
**Algorithm 1. Test time의 π0.7 prompting**

| 단계 | 연산 |
|---:|---|
| 1 | **입력:** 초기 observation o₀, task instruction **lang**, episode metadata m, control mode c |
| 2 | subtask **rawtext**를 초기화한다(high-level policy 또는 coaching에서 획득). |
| 3 | g★ ~ pψ(g★ \| o₀, **rawtext**, m) |
| 4 | C = {**lang**, **rawtext**, g★, m, c} |
| 5 | aₜ:ₜ₊H ~ πθ(a \| oₜ₋T:ₜ, C) *(선택 사항: CFG)* |
| 6 | t = 0, 1, 2, …에 대해 반복한다. |
| 7 | **rawtext**가 바뀌었거나 Δ-second timer가 경과했다면: |
| 8 | g★ ~ pψ(g★ \| oₜ, **rawtext**, m) *(non-blocking, async)* |
| 9 | C = {**lang**, **rawtext**, g★, m, c} |
| 10 | 마지막 추론 이후 Ĥ step이 경과했다면: |
| 11 | aₜ:ₜ₊H ~ πθ(a \| oₜ₋T:ₜ, C, aₜ:) *(RTC를 사용하는 async)* |
| 12 | aₜ를 실행한다. |

# 8. 로봇 시스템 세부 사항

**P2-015 (source lines 427–435)**  
FIGURE fig:robots: **실험에 사용한 일부 로봇의 예시.** 양팔 이동형 manipulator(왼쪽), 고정형 양팔 로봇(가운데), cross-embodiment 실험에 사용하는 양팔 UR5e setup(오른쪽)을 포함한 다양한 로봇에서 π0.7을 평가한다.

**P2-016 (source lines 437–443)**  
FIGURE fig:multi_task_film_strip: **선별한 평가 작업의 예시.** 여러 작업에서 π0.7을 평가하며, 그중 horizon이 더 긴 두 작업을 여기에 시각화한다. “Take Out Trash” 같은 일부 작업에서는 “take out the trash”와 같은 대략적인 instruction만 제공해도 π0.7이 장기 horizon 작업 전체를 수행한다. “Toasting a Bagel”처럼 π0.7 학습 데이터에 나타나지 않는 다른 작업에서는 π0.7의 강력한 언어 지시 수행 능력을 활용할 수 있다. 즉, 작업을 단계별로 분해한 일련의 상세 instruction으로 모델을 coaching하여 작업을 수행하게 한다.

**P2-017 (source lines 445–447)**  
π0.7을 다양한 로봇 플랫폼(Figure fig:robots)에 배포한다. 여기에는 6 DoF 팔 두 개를 장착한 양팔 이동형 manipulator, 경량 6 DoF 팔을 장착한 고정형 양팔 manipulator(“BiPi”), 그리고 cross-embodiment 실험에 사용하는 Robotiq gripper 장착 양팔 UR5e 시스템이 포함된다. 추가적인 일반화 및 언어 지시 수행 실험에는 BiPi 플랫폼과 같은 팔을 사용하는 단일 팔 6 DoF 시스템을 사용한다. 데이터의 상당 부분이 BiPi 플랫폼과 유사한 팔로 수집되었지만, cross-embodiment 시험에 사용하는 UR5e 팔은 훨씬 길고 morphology가 다르며 무게도 훨씬 무겁다. 실제로 UR5e 팔은 팔의 형상, 테이블 위 배치 방식(한쪽 가장자리가 아니라 양옆), gripper와 finger의 형상 때문에 서로 다른 manipulation 전략을 사용해야 하므로, 이 플랫폼으로의 cross-embodiment transfer는 상당한 난제이다. 모든 manipulator는 parallel-jaw gripper를 사용한다. UR5e 로봇은 20Hz로 작동하고, 다른 모든 로봇은 50Hz로 작동한다. 각 로봇에는 정면 카메라와 각 팔의 손목 카메라가 있으며, 이동형 로봇에는 후면 카메라도 있다. π0.7 모델의 action output은 단순한 PD controller를 통해 각 로봇에 적용한다. end-effector movement를 명령할 때는 numerical inverse kinematics를 적용하여 target end-effector pose를 target joint position으로 변환한다.

**P2-018 (source lines 449–455)**  
FIGURE fig:distillation_results: **즉시 사용 가능한 기민성.** π0.7은 별도 조정 없이도 매우 다양한 고난도 dexterous task를 수행할 수 있다. π*₀.₆의 작업(윗줄)과 “Robot Olympics” 실험의 작업을 포함한 여러 다른 dexterous task(아랫줄)를 고려한다. π*₀.₆의 작업에는 success rate와 normalized throughput(specialist model 대비)을 보고하며, raw throughput은 시간당 성공 횟수를 뜻한다. 다른 작업에는 task progress를 보고한다. 동일한 π0.7 모델이 각 작업별로 π*₀.₆ 또는 π₀.₆에 post-training된 specialist policy의 성능과 대등하며, 다양한 세탁물 접기와 상자 조립에서는 RL specialist보다 더 높은 throughput까지 달성한다.

**P2-019 (source lines 457–463)**  
FIGURE fig:distillation_ablations: **Prompt 구성과 평가 데이터가 즉시 사용 가능한 성능에 미치는 영향.** π0.7을 두 ablation과 비교한다. 하나는 context에 episode metadata를 포함하지 않는 π0.7 (no metadata)이고, 다른 하나는 학습 중 자율 평가 episode의 데이터를 포함하지 않는 π0.7 (no eval data)이다. π0.7은 모든 경우에 π0.7 (no metadata)와 π0.7 (no eval data)를 능가하며, 특히 throughput 격차가 가장 크다. 여기서 throughput(successes/hour)은 π0.7을 기준으로 정규화한다.

**P2-020 (source lines 465–471)**  
FIGURE fig:memory: **Memory가 필요한 작업.** π0.7은 이전 context를 명시적으로 추적해야 하는 작업도 수행할 수 있으며, MEM 논문의 일부 작업에 memory를 적용해 fine-tuning한 specialist policy와 비슷하거나 더 나은 성능을 달성한다.

**P2-021 (source lines 473–479)**  
FIGURE fig:instruction_following: **새로운 환경에서의 폭넓은 instruction following.** 보지 못한 주방 4곳과 침실 2곳에서 각각 3~6개의 open-ended instruction sequence를 수행하는 14개 instruction following scenario로 π0.7을 평가한다. 모든 평가에서 올바르게 수행한 instruction이 전체 instruction에서 차지하는 비율인 instruction following success rate를 보고한다. π0.7은 전반적으로 π₀.₅와 π₀.₆을 크게 능가하고 높은 절대 success rate를 달성한다.

**P2-022 (source lines 481–486)**  
FIGURE fig:instruction_generalization: **복잡한 referential instruction 수행.** π0.7과 이전 모델은 모두 더 단순한 재배치 instruction에서 성공한다. 이 instruction에는 “pick up the spoon”, “put the spoon to the left of the fork”, “put the spoon to the right of the fork”가 포함된다. 그러나 π0.7은 복잡하고 이례적인 instruction에서 훨씬 우수하다. 여기에는 “pick up the largest bowl on the table”, “pick up the object I would use to eat soup”, “pick up the fruit on the largest plate”가 포함된다. 경량 world model이 생성한 subgoal 이미지를 포함하면(π0.7 (GC)) instruction following 성능이 더 높아져, π0.7이 복잡한 instruction을 훨씬 더 잘 수행한다.

**P2-023 (source lines 488–495)**  
FIGURE fig:compositional_generalization: **Instruction 수행을 통한 데이터셋 편향 극복.** π0.7의 향상된 언어 지시 수행 성능은 강한 데이터셋 편향을 깨뜨릴 수 있게 한다. 이전 모델은 데이터의 패턴과 상충하는 instruction을 따라야 하는 데이터 편향 challenge task에서 어려움을 겪는다. 예를 들면 식기를 쓰레기통에 넣고 쓰레기를 식기 수거함에 넣는 작업이다. 그러나 π0.7은 이러한 강한 편향을 깨뜨리면서도 작업을 수행할 만큼 instruction을 잘 따를 수 있다. 특히 “Reverse Fridge to Microwave” 작업에서는 world model의 subgoal 이미지를 context에 포함하는 것(π0.7 (GC))이 성공에 결정적이다.

# 9. 실험 평가

**P2-024 (source lines 497–500)**  
실험에서는 π0.7이 다양한 context modality를 활용하여 여러 데이터 소스로부터 얼마나 강한 즉시 사용 가능한 성능, 폭넓은 일반화, 더 효과적인 transfer를 이끌어낼 수 있는지 평가한다. 구체적으로 π0.7이 복잡하고 dexterous한 작업을 별도 조정 없이 얼마나 잘 수행하는지, 특히 더 특화된 RL-finetuned 모델과 비교해 연구한다(7.1절). 다양한 작업을 수행하도록 instruction을 유연하게 따르는 능력을 평가하고(7.2절), embodiment 사이의 transfer 능력을 연구하며(7.3절), 이전에 보지 못한 방식으로 skill을 조합해 새로운 작업을 수행하는 능력을 시험한다(7.4절). 마지막으로 로봇 데이터셋의 작업 및 context 다양성이 증가할 때 π0.7의 성능이 어떻게 scale하는지 통제 실험으로 연구한다(7.5절).

## 9.1 까다로운 작업에서의 즉시 사용 가능한 성능

**P2-025 (source lines 502–506)**  
**π0.7은 작업별 post-training 없이 dexterous task에서 높은 성능을 달성한다.** 첫 번째 실험에서는 학습 데이터에서 본 적은 있지만 최대한 견고하고 효율적으로 수행하는 것이 목표인 dexterous task를 π0.7이 얼마나 잘 숙달하는지 연구한다. 이는 이전 로봇 파운데이션 모델에 의외로 어려운 문제이다. 범용 pre-training을 사용하더라도 최고 성능의 policy는 흔히 특정 downstream task에 맞춰 fine-tuning된다. 여기서는 다음 질문에 답하고자 한다. 범용 π0.7 모델이 여러 dexterous manipulation task에서 작업별 fine-tuned 모델의 성능과 대등할 수 있는가?

**P2-026 (source line 508)**  
Figure fig:distillation_results의 작업을 사용한다. 여기에는 이전에 RL 학습 π*₀.₆ 모델 평가에 사용한 espresso 만들기, 상자 조립, 세탁물 접기 작업이 포함되며, 단일 범용 π0.7 모델의 속도와 견고성을 개별 RL-finetuned specialist π*₀.₆ 모델과 직접 비교할 수 있다. 이전 “Robot Olympics” 실험의 일부 작업(땅콩버터 샌드위치 만들기, 셔츠 뒤집기, 문을 통과해 주행하기)과 애호박 한 개를 완전히 썰기, 여러 과일과 채소(애호박, 오이, 당근) 껍질 벗기기, 쓰레기통의 쓰레기봉투를 교체하는 장기 horizon 작업 등 다른 dexterous task도 연구한다. π0.7은 별도 조정 없이도 논문에서 고려한 모든 작업에서 π*₀.₆ 공개판의 RL specialist와 경쟁할 만한 성능을 달성하며(Figure fig:distillation_results, 첫째 줄), 어려운 세탁물 및 상자 조립 작업에서는 throughput으로 specialist를 능가하기까지 한다. 또한 여러 다른 dexterous task에서 π0.7을 π₀.₆ 위에 학습한 SFT specialist와 비교한 결과, π0.7은 다시 모든 specialist policy의 성능에 근접한다(Figure fig:distillation_results, 둘째 줄).

**P2-027 (source line 510)**  
π0.7의 학습 레시피가 성능에 미치는 영향을 이해하기 위해 π*₀.₆ 공개판의 작업에서 π0.7을 두 ablation과 추가로 비교한다. π0.7 (no eval data)는 모든 자율 평가 episode를 학습에서 제외하므로, RL 학습 policy 같은 강력한 policy의 agent rollout을 distillation하는 이점을 얻을 수 없다. π0.7 (no metadata)는 context에서 episode metadata를 제외한다. Figure fig:distillation_ablations의 결과는 π0.7이 모든 작업에서 두 ablation을 크게 능가함을 보여준다. policy 평가 데이터의 품질은 매우 다양할 수 있으므로, 이 데이터로 학습하면서 풍부한 metadata로 고품질 행동과 저품질 행동을 구분하는 것은 π0.7이 이 모든 까다로운 작업에서 강한 성능을 내는 데 결정적이다.

**P2-028 (source lines 512–514)**  
**π0.7은 fine-tuning 없이 memory가 필요한 작업에서 높은 성능을 달성한다.** 이 실험에서는 이전 observation을 명시적으로 추적해야 하는 작업을 π0.7이 얼마나 잘 수행하는지 연구한다. 동일한 단일 π0.7 모델을 별도 조정 없이 사용해 `MEM`에서 사용한, memory를 갖춘 작업별 fine-tuned π₀.₆ 버전과 비교한다. π0.7은 모든 작업에서 fine-tuned specialist와 비슷하거나 더 나은 성능을 달성한다(Figure fig:memory).

## 9.2 Instruction following

**P2-029 (source lines 516–519)**  
다음 실험에서는 π0.7이 언어 instruction을 얼마나 잘 따르는지 연구한다. 여기에는 다양한 context를 실행하고 학습 데이터와 체계적으로 다른 referential instruction을 따르는 능력이 포함된다. 실험은 로봇이 수행할 수 있는 작업이 많은 어수선한 환경에 특히 초점을 맞추며, 성공하려면 π0.7이 제공된 instruction에 세심하게 주의를 기울여야 한다. π0.7은 이전 모델 π₀.₅와 π₀.₆보다 크게 향상된 instruction following 능력을 보인다.

**P2-030 (source lines 521–523)**  
**π0.7은 유연한 prompting을 통해 매우 다양한 작업을 수행할 수 있다.** 언어 지시 수행은 로봇 파운데이션 모델의 악명 높은 난제였으며, 특히 학습에서 본 instruction에 직접 대응하지 않는 open-vocabulary instruction이 어렵다. 이 실험에서는 π0.7 역량의 폭을 연구하여 다음 질문에 답하고자 한다. π0.7은 이전 모델보다 더 다양한 언어 instruction을 더 잘 처리할 수 있는가? 학습 데이터에 없던 주방 4곳과 침실 2곳에서 다양한 instruction으로 π0.7을 평가한다(Figure fig:instruction_following). 각 실험은 로봇이 특정 goal을 달성하기 위해 3~6단계의 instruction sequence를 따를 수 있는지 시험한다. 작업에는 물건 재배치와 정돈, 가구와의 상호작용, 흘린 내용물 청소 등 주방 및 침실 환경의 현실적인 여러 작업이 필요하다. 새로운 시험 환경과 다양한 instruction의 조합은, 본 적 있는 환경에서도 단순한 instruction 수행에 어려움을 겪을 수 있는 로봇 파운데이션 모델에 큰 난제이다. π0.7은 높은 전체 instruction following success rate를 기록하며 π₀.₅와 π₀.₆을 크게 능가한다.

**P2-031 (source lines 525–526)**  
**π0.7은 out-of-distribution referential instruction을 처리할 수 있다.** 학습 데이터가 폭넓고 다양하기 때문에 시험 instruction이 얼마나 *새로운지* 정량화하기는 일반적으로 어렵다. 다음 실험에서는 이례적이거나 객체를 관습적이지 않은 방식으로 지칭하거나 공간 관계 이해가 필요한 instruction 집합을 의도적으로 설계했다. Figure fig:instruction_generalization에서는 객체 재배치 instruction 집합을 *standard*와 *complex* instruction으로 나누어 π0.7과 이전 모델을 비교한다. standard instruction은 학습 데이터의 언어 instruction과 비슷한 방식으로 표현한다. complex instruction은 “pick up an object I would use to eat soup” 또는 “pick up the fruit on the largest plate”처럼 이례적인 언어나 복잡한 공간 참조를 사용한다. 이 실험에서는 앞서 설명한 경량 world model이 생성한 subgoal 이미지의 사용 여부에 따라서도 π0.7을 평가한다. π0.7은 complex instruction에서 이전 모델보다 향상되며, subgoal 이미지를 사용하면 world model의 semantic understanding을 가져와 성능이 더욱 높아진다.

**P2-032 (source lines 528–534)**  
FIGURE fig:cross_embodiment: **Cross-embodiment transfer.** 왼쪽: π0.7과 이전 모델 모두 더 단순한 재배치 또는 위치 조정 유형의 작업에서 별도 조정 없이 강한 cross-embodiment transfer를 달성한다. 예를 들어 “Table Setting” 작업의 데이터는 다양한 로봇으로 수집했고, 작업은 고정형 양팔 로봇에서 시험했다. 모든 모델이 우수한 성능을 냈다. 양팔 UR5e 로봇에서 더 작은 고정형 양팔 로봇으로 transfer해야 하는 작업(“Bag In Backpack” 및 “Organize Tupperware”)은 source robot이 target robot보다 크고 무거운 단 한 종류뿐이어서 embodiment 격차가 더 크다. 여기서 π₀.₅는 성능이 매우 낮았지만 π₀.₆은 여전히 상당히 우수했다. “Shirt Bagging” 작업에서 더 작은 고정형 양팔 로봇에서 UR5e로 transfer하면 embodiment 격차가 가장 커지며, 여기서는 π0.7 모델이 이전 모델을 크게 능가한다. 오른쪽: 수건과 티셔츠를 접어야 하는 더 dexterous한 작업에서는 embodiment 격차가 한층 더 큰 난제가 된다. 이 작업의 데이터는 더 작은 고정형 양팔 로봇으로 수집했고, 평가는 더 큰 양팔 UR5e 플랫폼에서 수행했다. π0.7은 이 작업을 성공적으로 transfer했으며, 경량 world model이 생성한 visual subgoal 이미지를 사용하자 성능이 더욱 향상되었다. 실제로 task progress는 다양한 로봇을 조작해 본 가장 숙련된 인간 teleoperator들이 UR5e에서 이 작업을 처음 시도했을 때의 “zero-shot” 성능과 대등하다.

**P2-033 (source lines 536–540)**  
**π0.7은 데이터셋 편향을 거스르는 instruction을 따를 수 있다.** 데이터셋 편향은 instruction following의 큰 난제이다. 로봇이 특정 scene에서 항상 같은 행동을 한다면, 그러한 데이터로 학습한 모델은 해당 scene에서 언어를 무시하고 데이터에서 본 행동을 맹목적으로 복제하는 경우가 많다. 다음 실험에서는 이 문제가 발생하는 scenario를 구성하고, π0.7에 prompt를 제공하여 데이터셋의 자연스러운 편향을 *거스를* 수 있는지 시험한다. “Reverse Bussing”과 “Reverse Fridge to Microwave”라는 두 작업을 구성했다. 데이터셋에서 “bussing” 작업은 쓰레기를 쓰레기통에 넣고 식기를 식기 수거함에 넣는다. “Reverse Bussing”에서는 반대로 쓰레기를 식기 수거함에 넣고 식기를 쓰레기통에 넣으라고 로봇에 요구한다. “Fridge to Microwave” 작업은 냉장고에서 음식을 꺼내 전자레인지에 넣어야 하며, 반대 방향의 데이터는 수집하지 않았다. 시험 시 이 작업의 “reverse” 버전인 “Reverse Fridge to Microwave”에서는 로봇에 prompt를 제공해 전자레인지의 음식을 냉장고로 옮기게 하여 데이터셋의 편향을 위반한다. Figure fig:compositional_generalization의 결과에서 π0.7은 이 작업들에서 이전 모델보다 크게 향상된다. 이는 π0.7의 언어 지시 수행 능력이 훨씬 우수하고, 이 작업의 데이터 편향을 극복할 만큼 instruction에 충분히 주의를 기울임을 시사한다. “Reverse Fridge to Microwave”에서는 생성된 subgoal 이미지에 conditioning하는 것(π0.7 (GC))이 성공에 결정적이다. world model이 web-scale image generation pre-training을 활용하여 text instruction에 근거한 subgoal을 효과적으로 생성할 수 있기 때문이다.

## 9.3 Cross-embodiment transfer

**P2-034 (source lines 543–545)**  
여러 모델이 서로 다른 다수의 로봇 embodiment 데이터를 사용해 왔지만, source embodiment의 복잡한 작업을 해당 작업을 한 번도 본 적 없는 target robot으로 zero-shot transfer하는 것은 큰 난제이다. 이 실험에서는 cross-embodiment transfer가 π0.7의 *emergent* property인지 연구한다. 즉, π0.7은 작업별 데이터가 전혀 수집되지 않은 로봇 embodiment로 역량을 직접 transfer할 수 있는가?

**P2-035 (source line 547)**  
여러 작업에서 π0.7은 target robot의 학습 데이터가 전혀 없는 작업을 target embodiment에서 아무 조정 없이 성공한다. embodiment 차이가 비교적 작을 때는 π₀.₅와 π₀.₆ 모델도 어느 정도 emergent cross-embodiment transfer를 보인다. 그러나 로봇 morphology의 격차가 커질수록 복잡한 skill을 효과적으로 transfer하려면 전략을 더 크게 바꿔야 한다. 이런 경우 π0.7은 이전 모델을 크게 능가하며, 아래에서 설명하듯 셔츠 접기 작업에서는 인간 teleoperator의 “zero-shot” 성능과도 대등하다. 아래 실험 결과에는 joint-space control을 적용한다. 이전 모델에서는 end-effector control이 눈에 띄는 성능 향상을 내지 못했기 때문이다(appendix 참조).

**P2-036 (source lines 550–551)**  
**객체 재배치 작업의 zero-shot cross-embodiment transfer.** 먼저 특정 작업의 데이터 수집에 사용한 로봇과 다른 로봇에서 π0.7을 시험하는, 비교적 단순한 객체 재배치 작업 집합을 연구한다. 결과는 Figure fig:cross_embodiment에 제시한다. 첫 작업인 “Table Setting”의 데이터는 이동형, 고정형, 단일 팔 시스템 등 여러 로봇 유형으로 수집했다. 모델이 여러 로봇에서 작업의 공통 구조를 추론할 수 있으므로 cross-embodiment transfer에 가장 유리한 설정이다. 고정형 양팔 로봇 시스템에서 평가한 결과, 모든 방법이 강한 cross-embodiment transfer 징후를 보인다. 그러나 embodiment 격차를 더 크게 하여 모든 데이터를 더 큰 양팔 UR5e 플랫폼에서 수집한 뒤 더 작은 고정형 양팔 플랫폼에서 policy를 시험하면(“Bag In Backpack” 및 “Organize Tupperware”), π₀.₅의 성능은 크게 저하되지만 π₀.₆과 π0.7은 여전히 강한 성능을 달성한다. 이어 embodiment 격차를 더 키워 더 작은 고정형 양팔 플랫폼에서 데이터를 수집하고 *단일 팔* UR5e 플랫폼에서 평가한 작업(“Shirt Bagging”)의 transfer를 연구한다. target robot은 팔이 하나뿐이고 훨씬 크고 무겁기 때문에 상당히 다른 전략이 필요하다. 여기서는 π0.7이 이전 모델을 크게 능가한다.

**P2-037 (source lines 553–559)**  
FIGURE fig:human_vs_policy: **Cross-embodiment transfer는 target embodiment에 적응한 emergent strategy를 만들어낸다.** (a) source robot에서 인간 teleoperator는 한 팔로 가방을 벌린 채 다른 팔로 물건을 삽입한다. 반면 UR5e target robot에서 π0.7은 로봇의 더 긴 reach에 적합한 단일 팔 pick-and-place 전략을 발견한다. (b) source robot에서 인간 teleoperator는 기울어진 end-effector로 셔츠에 접근하지만, π0.7은 UR5e에서 더 큰 로봇의 팔 배치에 적합한 수직 grasp를 생성한다. 두 경우 모두 policy는 source 행동의 복제를 넘어 target embodiment에 더 적합한 작업 manipulation 전략을 발견한다.

**P2-038 (source line 561)**  
특히 성공적인 transfer를 위해서는 source 행동을 단순히 복제하기보다 target morphology에 맞는 새로운 manipulation 전략을 policy가 발견해야 하는 경우가 많다. 예를 들어 더 짧은 고정형 양팔 로봇은 한 팔로 가방을 벌린 채 다른 팔로 물건을 넣어야 하지만, 더 높은 UR5e 팔은 단일 팔 pick-and-place로 같은 작업을 완수할 수 있다(Figure fig:human_vs_policy (a)). 이처럼 morphology 격차가 큰데도 모델은 각 embodiment에 적절한 전략을 적용하여, 원래 로봇의 motion 모방을 넘어서는 cross-embodiment transfer를 입증한다.

**P2-039 (source lines 567–573)**  
FIGURE fig:air_fryer_coaching: **언어 coaching 예시.** 단계별 verbal instruction을 제공하여 π0.7에 새 작업을 “가르칠” 수 있다. 언어 지시 수행 능력 덕분에 π0.7은 사용자 instruction 아래 새로운 작업을 성공적으로 수행할 수 있으며, 이어 이 instruction을 사용해 π0.7에 prompt를 제공하는 high-level policy를 학습하면 작업을 완전 자율로 수행하게 할 수 있다.

**P2-040 (source lines 575–581)**  
FIGURE fig:long_horizon_task_generalization: **새로운 장기 horizon 작업을 수행하도록 coaching하기.** π0.7은 생소한 skill에서도 언어 instruction을 효과적으로 따를 수 있으므로, 언어와 생성된 subgoal 이미지에 conditioning할 때(π0.7 (GC)) 본 적 없는 여러 장기 horizon 작업을 수행하도록 “coaching”할 수 있다. 이전 모델은 일반적으로 coaching command를 따르는 데 필요한 언어 지시 수행 능력이 부족하여 성능이 매우 낮다.

**P2-041 (source lines 583–589)**  
FIGURE fig:coaching: **Coaching을 통한 새로운 자율 역량 획득.** 본 적 없는 여러 작업에서 수집한 coaching episode를 사용하여, coaching episode에 맞춰 π0.7에 자동으로 prompt를 제공하는 high-level policy를 학습할 수 있다. 이를 통해 teleoperation이나 다른 종류의 low-level action 데이터를 추가로 전혀 수집하지 않고도, 실시간 인간 coaching을 받는 policy(π0.7 (coaching))의 성능에 근접하는 완전 자율 policy(π0.7 (autonomous))를 이 작업들에 만들 수 있다.

**P2-042 (source lines 591–597)**  
FIGURE fig:task_generalization: **새로운 단기 horizon 작업 수행.** π0.7은 어떤 작업에 대해서도 데이터를 수집하지 않았는데도, 밥솥에 쌀 퍼 넣기, gear set 및 탁상용 선풍기 같은 여러 물체 돌리기, 자와 헤드폰 같은 물체를 천으로 닦기 등 여러 새로운 단기 horizon 작업을 별도 조정 없이 수행할 수 있다. 언어 instruction에 직접 conditioning한 경우(π0.7)와 생성 image goal에 conditioning한 경우(π0.7 (GC))에 π0.7은 대체로 동등하게 강한 성능을 보인다.

**P2-043 (source lines 599–600)**  
**Dexterous task의 zero-shot cross-embodiment transfer.** 세탁물 접기 같은 dexterous task는 cross-embodiment transfer에 더 큰 난제를 제기한다. 이러한 작업에는 단순히 물체를 grasp하고 위치를 바꾸는 것보다 정밀한 manipulation skill이 필요하다. 티셔츠를 성공적으로 접으려면 정밀한 grasp와 placement의 sequence가 필요하며, 올바른 grasp angle은 로봇의 reachable workspace와 gripper orientation에 따라 달라질 수 있다. 접기 데이터 대부분은 경량 고정형 양팔 로봇으로 수집했다(Figure fig:robots). 양팔 UR5e 시스템으로는 세탁물 접기 데이터를 전혀 수집하지 않았다. 이 시스템의 morphology, reachable workspace, dynamics(예: 더 높은 internal inertia)는 세탁물 접기 데이터 수집에 사용한 로봇과 크게 다르다. UR5e는 일반적으로 teleoperation이 더 어렵고 매우 정밀한 grasp에 덜 적합했으며, 이는 이 로봇으로 세탁물을 접으려면 manipulation 전략을 바꿔야 함을 시사한다.

**P2-044 (source lines 603–609)**  
FIGURE fig:generalization_and_conditioning: **다양한 context와 데이터에 따른 일반화 성능 scaling.** 왼쪽: π0.7 (with metadata)은 더 큰 데이터셋으로 학습할수록 평균 데이터 품질이 실제로 낮아지는 경우에도 지속적으로 성능이 향상된다. 반면 풍부한 conditioning information 없이 학습하면, π0.7 (without metadata)은 품질이 낮은 데이터가 더 많이 추가될수록 오히려 성능이 저하될 수 있다. 오른쪽: 작업 다양성이 가장 높은 로봇 데이터를 제외하고 π0.7을 학습하면 성능이 크게 저하된다. 이는 π0.7이 로봇 데이터의 작업 다양성을 활용하여 compositional task generalization을 크게 향상할 수 있음을 시사한다.

**P2-045 (source lines 612–613)**  
π0.7은 양팔 UR5e 시스템에서 수건과 셔츠를 모두 성공적으로 접었다(Figure fig:cross_embodiment, 오른쪽). source robot(Figure fig:robots의 고정형 양팔 로봇)에서 인간 operator는 천을 들어 올리기 전에 테이블에 고정하려고 기울어진 end-effector로 접근하는 경우가 많다. 반면 UR5e에서 π0.7은 팔의 kinematics에 더 적합한 수직 grasp를 사용한다. 이는 source robot의 학습 데이터와는 다르지만 target embodiment에 더 적합한 전략이다(Figure fig:human_vs_policy (b)). world model의 subgoal image generation을 사용하면 성능이 크게 향상되는 것도 확인했다(plot의 π0.7 (GC)). world model이 source robot과 target robot 사이의 시각적 analogy를 더 효과적으로 구성할 수 있기 때문이다. 생성된 subgoal은 target robot에 어떤 종류의 grasp와 의류 configuration이 합리적인지 예측하고, 모델은 더 나은 action을 선택하기 위한 단서로 이 추가 context를 통합한다.

**P2-046 (source line 616)**  
이 결과에 맥락을 부여하기 위해 숙련된 teleoperator 10명을 대상으로 인간 연구를 수행했다. 이들은 모든 로봇을 합쳐 평균 375시간의 teleoperation 경험이 있으며, 경험 기준 모두 상위 2%에 속한다. policy와 마찬가지로 이 operator들은 source embodiment에 폭넓은 경험이 있지만 양팔 UR5e 시스템에서 셔츠 접기를 시도한 적은 없었으므로, 인간과 policy 모두에 zero-shot cross-embodiment transfer 설정이다. 인간 operator는 task progress 90.9%와 success rate 80.6%를 달성했고, π0.7은 task progress 85.6%와 success rate 80%를 달성하여 expert operator와 대등한 성능을 보였다. 이 비교가 부각하는 강력한 cross-embodiment transfer 성능은 과학적으로 흥미로우며 실용적인 함의도 있다. dexterous skill을 teleoperation하기 쉬운 경량 저비용 플랫폼*에서* 인간 시연 데이터 수집이 훨씬 비싸고 어려운 고하중 산업용 팔*로* transfer할 수 있다는 것이다. 인간 연구 설정과 결과의 자세한 내용은 appendix에 제시한다.

## 9.4 Compositional task generalization

**P2-047 (source lines 618–623)**  
다음 실험에서는 π0.7이 학습에서 본 skill을 compositional하게 일반화하여 새로운 작업을 얼마나 잘 수행하는지 연구한다. 이는 로봇 파운데이션 모델의 일종의 “grand challenge”로 여겨져 왔다. 이전 모델은 semantic concept에 대한 일반화, 예를 들어 보지 못한 text label을 가진 객체에 손을 뻗는 능력은 입증했지만, 새로운 작업 수행은 좀처럼 달성하지 못했다. 일부 단기 horizon 작업에서는 해당 작업을 위해 명시적으로 수집한 데이터가 전혀 없어도 π0.7이 완전히 별도 조정 없이 잘 작동한다. 이러한 작업은 헤드폰을 천으로 닦거나 탁상용 선풍기를 돌리는 것처럼 낯선 물체를 새로운 방식으로 조작한다(Figure fig:task_generalization). 더 긴 horizon의 복잡한 작업에서는 π0.7의 instruction following 능력을 사용해 언어로 작업 수행을 “coaching”할 수 있다. 이는 추가 학습 데이터를 수집하지 않고도 π0.7에 새로운 작업을 가르치는 흥미로운 방법이다.

**P2-048 (source lines 625–626)**  
**π0.7은 새로운 단기 horizon 작업을 별도 조정 없이 수행할 수 있다.** π0.7은 각 작업을 위해 특별히 수집한 로봇 데이터가 없는데도 French press의 plunger 누르기, 밥솥에 쌀 퍼 넣기, 흔한 사무용품 닦기, 여러 articulated item 돌리기 같은 단기 horizon 작업을 별도 조정 없이 수행할 수 있다(Figure fig:task_generalization). π0.7은 매우 다양한 skill을 유연하게 조합할 수 있으므로, 원하는 행동을 얻도록 prompt를 제공하는 것만으로 새로운 단순 작업을 수행하게 할 수 있는 경우가 많다는 점은 매우 고무적이다.

**P2-049 (source lines 628–629)**  
**π0.7은 오직 언어를 통한 coaching으로 새로운 장기 horizon 작업을 수행할 수 있다.** π0.7에 직접 prompt를 제공해 새로운 단기 horizon 작업을 수행하게 할 수 있지만, 고구마 요리처럼 본 적 없는 장기 horizon 작업을 수행하라고 단순히 요청하는 것은 작동하지 않는다. π0.7이 높은 수준의 즉시 사용 가능한 일반화 능력을 보이더라도, 이런 작업은 여러 stage에 걸쳐 최대 5분의 상호작용이 필요하므로 지나치게 복잡하다. 그러나 π0.7의 언어 지시 수행 능력은 이러한 작업을 모델에 가르칠 흥미로운 새 경로를 제공한다. 로봇이 학습하길 원하는 복잡한 skill마다 demonstration data를 제공하는 대신, 사람에게 작업을 가르치듯 언어로 새 작업 수행을 “coaching”할 수 있다(Figure fig:air_fryer_coaching). 현실적인 다단계 주방 작업을 여러 개 설정했다. (1) “Loading an Air Fryer”: air fryer로 고구마 요리하기, (2) “Unloading an Air Fryer”: air fryer에서 물건 쏟아내기, (3) “Toasting a Bagel”: toaster로 bagel 굽기이다. 인간 데이터와 외부 데이터셋의 다른 context에서 유사한 기기를 본 적은 있지만, 각 경우 로봇 데이터에는 해당 작업의 학습 episode가 전혀 없었다. 그러나 사람은 “pick up the sweet potato”와 “open the air fryer” 같은 단계별 instruction으로 로봇의 작업 수행을 안내할 수 있다. π0.7 coaching 결과와 비교는 Figure fig:long_horizon_task_generalization에 제시한다. 중요한 점은 어떤 모델도 이 특정 작업들의 *action-level* 데이터를 갖고 있지 않고, “coaching” episode의 환경과 작업도 완전히 본 적 없다는 것이다. π0.7은 이전 방법보다 훨씬 효과적으로 coaching되어 이 모든 작업을 수행할 수 있으며, 생성된 subgoal 이미지에 conditioning하면 더욱 효과적이다.

**P2-050 (source lines 631–632)**  
**Coaching data는 π0.7에 새로운 역량을 부여할 수 있다.** π0.7은 coaching을 통해 새로운 작업을 수행할 수 있으므로, coaching data의 단계별 instruction을 사용해 작업을 수행하는 동안 적절한 언어 instruction으로 π0.7에 prompt를 제공하는 high-level language policy를 학습할 수 있다. 이로써 π0.7은 추가 teleoperation data를 전혀 수집하지 않고도 완전히 본 적 없는 장기 horizon 작업을 수행할 수 있다. 다섯 가지 작업에 대한 이 실험의 결과는 Figure fig:coaching에 제시한다. 모든 작업에서 모델에 prompt를 제공해 작업을 수행하도록 하여 수집한 coaching episode(π0.7 (coaching))의 성능에 대략 대등한 autonomous policy(π0.7 (autonomous))를 성공적으로 학습할 수 있다.

## 9.5 π0.7은 다양하고 품질이 혼재된 데이터에서 효과적으로 학습할 수 있는가?

**P2-051 (source lines 636–638)**  
마지막 실험에서는 π0.7이 크고 다양한 데이터셋을 효과적으로 활용할 수 있는지, 그리고 데이터셋 다양성이 증가할 때 성능이 향상되는지 이해하기 위해 일련의 통제된 ablation study를 수행한다. 이러한 모델의 성능은 매우 많은 요인에 좌우되고, 초대형 데이터셋을 “다양성” ablation이 가능하도록 명확히 분할하기가 매우 어렵기 때문에 이 질문에 확정적으로 답하기는 어렵다. 이 질문을 어느 정도 이해하기 위해 먼저 더 크지만 품질이 더 혼재된 데이터셋으로 학습할 때 π0.7이 본 적 있는 작업에서 계속 향상되는지 연구한다. 이어 π0.7이 작업 다양성이 높은 데이터셋을 활용해 일반화를 향상할 수 있는지 연구한다.

**P2-052 (source lines 640–641)**  
**π0.7은 품질이 혼재된 데이터에서 효과적으로 학습할 수 있다.** 다양한 로봇 데이터에서 효과적으로 학습하는 것은 지금까지 로봇 policy 학습의 큰 난제였다. 설계자는 일관된 전략의 고품질 데이터셋을 얻기 위해 데이터를 신중하게 filtering하거나 curation하는 경우가 많다. 그러나 data filtering은 노동집약적이고 작업별로 이루어지며, 결국 유용한 정보를 많이 버리게 된다. 이 실험에서는 다음 질문에 답하고자 한다. π0.7은 다양한 manipulation 전략을 담은 데이터에서 더 많이 학습할 수 있는가?

**P2-053 (source lines 643–644)**  
이 질문을 연구하기 위해 Figure fig:distillation_results에서 살펴본 “Laundry (T-Shirts and Shorts)” 작업을 고려한다. 인간 operator가 수집한 데이터에 접기 품질과 속도를 기준으로 annotation을 부여하고, 데이터셋을 네 bucket으로 나눴다. (1) 품질과 속도 기준 상위 30%, (2) 상위 50%, (3) 상위 80%, (4) 전체 데이터이다. 이어 각 bucket의 데이터로 episode metadata를 사용하거나 사용하지 않고 새로운 π0.7 모델을 처음부터 학습했다(총 8개 모델). π0.7 (without metadata)은 더 크고 품질이 혼재된 데이터셋으로 학습할 때 오히려 나빠질 수 있지만, π0.7 (with metadata)은 데이터셋 크기가 커지면서 평균 데이터 품질이 낮아지는데도 데이터가 늘어날수록 계속 향상된다(Figure fig:generalization_and_conditioning, 왼쪽). 이는 다양한 prompting 방법이 모델 설계를 사실상 *더 scalable하게* 만든다는 뜻이다. 일반적인 방식으로 학습한 모델에는 해가 되는 저품질 데이터가 더 큰 데이터셋에 포함되더라도, 데이터셋이 커질수록 더 많은 이점을 얻기 때문이다. episode metadata는 π0.7 학습 중 대규모 데이터셋 내부의 서로 다른 데이터 품질과 전략을 효과적으로 구분하고, 시험 시 원하는 행동 mode에 prompt를 제공할 수 있게 한다.

**P2-054 (source lines 646–648)**  
**π0.7은 증가한 데이터셋 다양성을 더 나은 일반화 성능으로 전환할 수 있는가?** 이 질문을 연구하기 위해 Figure fig:task_generalization의 본 적 없는 단기 horizon 작업 중 일부에서 π0.7을 다음 ablation과 비교한다.

**P2-055 (source lines 649–652)**  
- **π0.7 (w/o most diverse 20%)**: π0.7에서 작업 다양성이 가장 높은 데이터 20%를 제거한다.
- **π0.7 (w/o random 20%)**: π0.7 데이터에서 무작위로 샘플링한 20%를 제거하여 π0.7 (w/o most diverse 20%)에 대한 데이터 양 통제 비교군으로 사용한다.

**P2-056 (source line 654)**  
π0.7 (w/o most diverse 20%)와 π0.7 (w/o random 20%)의 비교를 통해 두 모델이 같은 양의 데이터로 학습된 통제된 조건에서 작업 다양성이 높은 데이터의 영향을 이해할 수 있다. 모든 작업에서 π0.7과 π0.7 (w/o random 20%)는 π0.7 (w/o most diverse 20%)를 크게 능가한다. 이는 π0.7이 작업 다양성이 높은 데이터를 효과적으로 흡수하여, 그 데이터를 본 적 없는 단기 horizon 작업의 성능 향상으로 전환할 수 있음을 보여준다(Figure fig:generalization_and_conditioning, 오른쪽).
