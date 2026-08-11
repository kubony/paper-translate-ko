<!-- source: main.tex active lines 181-288 -->

[[FIGURE:fig:method:model|fig/pipeline_v2.pdf|\linewidth]]

**방법 개요.** (a) 외란하에서 position 및 force 명령을 추종하도록 reinforcement learning으로 학습한 통합 position-force policy의 architecture이다. (b) Force sensor 없이 본 연구에서 학습한 policy를 사용해 수집한 demonstration으로 구현되는 force-aware imitation learning이다. (c) end-effector와 robot base 모두에서 모델링한 force 상호작용을 위한 position 및 velocity 보상을 보여준다. (d) Policy 학습 중 다양한 contact 상황을 시뮬레이션하는 데 사용한, 샘플링된 force 명령과 외란을 시각화한다.

**다중 contact 모델링.** End-effector 이외의 다른 robot body part에 대해서도 [[REF:eq:pos_force_target]]의 정식화를 그에 맞게 확장할 수 있다. Robot base를 예로 들면, 일반적으로 base의 joint state가 아니라 velocity 또는 global position에 관심을 둔다. 이러한 경우 robot이 base velocity 명령으로 control된다고 가정하여 [[REF:eq:pos_force_target]]을 단순화할 수 있다. 구체적으로 velocity 및 force 명령 v_base^cmd = ẋ_base^cmd와 F_base^cmd, 그리고 외란 F_base^ext가 주어지면 [[REF:eq:impedance_general]]로부터 다음을 도출할 수 있다.

F_base = D(ẋ_base − ẋ_base^des) = D(v_base − v_base^des).  (1)

Base의 global position을 이용할 수 없으므로 position 항은 생략한다. 여기서 F_base = F_base^ext + (F_base^cmd − F_base^react)는 net force이며, [[REF:eq:pos_force_target]]을 다음과 같이 변환한다.

v_base^target = v_base^cmd + [F_base^ext + (F_base^cmd − F_base^react)] / D.  (2)

이 변환 후에는 [[REF:eq:base_pos_force]]에서 도출한 식을 사용하여 유사한 기본 control mode를 구현할 수 있다. 더 나아가 robot base에 작용하는 net force F_base를 end-effector에 대한 외력 F_base2ee로 변환하거나 그 반대로 변환함으로써, body part에 대한 외란과 force 명령을 end-effector로 변환하는 상황까지 이 정식화를 확장할 수 있다. 그러나 이러한 방법은 학습 복잡도가 높으므로, 본 연구에서는 end-effector와 robot base를 독립적으로 취급하는 데 초점을 맞추며 통합된 유도는 중요한 향후 연구로 남긴다.

요약하면, 능동 force와 수동 force를 모두 고려하여 legged robot의 end-effector 및 base 동작을 모델링하는 [[REF:eq:pos_force_target]]과 [[REF:eq:base_pos_force]]에 따라 reward를 제공하여 policy를 학습한다. 자세한 학습 설정과 모델은 [[REF:sec:learning]]에서 제시한다.

## 통합 force-position control policy 학습

먼저 observation, command, action 공간을 정의하여 제안한 통합 force-position control policy의 학습 과정을 상세히 설명한다.

구체적으로 robot의 observation o_t는 robot의 base orientation g_t^base, angular velocity ω_t^base, joint position q_t, joint velocity q̇_t, 이전 action a_{t−1}, command c_t^cmd, 그리고 foot clock timing θ_t^feet로 다음과 같이 정의한다.

o_t = [g_t^base, ω_t^base, q_t, q̇_t, a_{t−1}, c_t^cmd, θ_t^feet].

여기서 입력 command c_t^cmd = [v_base^cmd, x_ee^cmd, F_ee^cmd, F_base^cmd]는 base velocity, end-effector position, end-effector force, base force 명령을 포함한다. Quadrupedal robot에서는 네 가지 command 유형을 모두 고려한다. Humanoid robot에는 manipulation task에 사용할 gripper가 없으므로 locomotion command v_base^cmd와 base force command F_base^cmd만 고려한다. 출력 action a_t는 사전에 정의한 default pose에 더하는 residual이며, PD controller의 joint position target q_t^target은 다음과 같이 계산한다.

q_t^target = σ_a a_t + q^default,

여기서 σ_a는 policy 출력을 scaling하고 q^default는 표준 pose를 나타낸다.

**Policy 설계.** Policy 모델의 개요는 [[REF:fig:method:model]](a)에 제시한다. Policy 모델은 observation encoder, state estimator, actor의 세 module로 구성된다. Encoder는 observation history o_[t−H, …, t−1, t] (H = 32)를 처리하여 latent feature를 출력하고, 이 feature는 state estimator와 actor로 전달된다. 이어서 state estimator는 외력 F = F^ext + F^react, end-effector position, base velocity를 포함한 robot state를 예측한다. 이렇게 추정한 force는 원하는 특정 control 동작에서 command signal로 변환할 수 있다.

**Force 시뮬레이션.** 통합 force-position policy를 학습하기 위한 다양한 상황을 시뮬레이션하기 위해 [[REF:eq:pos_force_target]]과 [[REF:eq:base_pos_force]]에서 요구하는 position, velocity, force 명령과 외부 net force를 무작위로 샘플링한다. 입력 command와 외력의 범위는 [[REF:sec:appendix:cmd_details]]에 자세히 제시한다. 특히 reaction force F^react는 명시적으로 모델링하지 않고 net external force F = F^ext + F^react에 포함한다.

x^cmd의 샘플링 범위는 whole-body movement가 없을 때 arm의 원래 workspace를 약간 넘도록 설정하되, whole-body motion을 허용할 때 산출되는 x_ee^target이 operation limit 안에 유지되도록 한다.

학습 중에는 [[REF:fig:method:model]](d)에 나타난 것처럼 샘플링한 force를 target 값까지 선형적으로 증가시키고, 고정된 구간 동안 일정하게 유지한 뒤, 사전에 정의한 schedule에 따라 다시 0까지 감소시킨다. 짧은 zero-force 구간이 지난 후 새로운 force를 샘플링하고 이 cycle을 반복한다. 이 샘플링 전략은 policy를 다양한 control 조건에 노출하며, [[REF:sec:method:formulation]]에서 논의한 서로 다른 원하는 control 동작을 반영하여 하나의 policy가 다양한 control task 요구에 적응할 수 있게 한다.

**Policy 학습.** 두 단계의 학습 절차를 채택한다. 먼저 whole-body reaching과 locomotion에 초점을 맞춘 뒤, 무작위 force 명령과 외란을 도입한다. [[REF:sec:appendix:rl_training_details]]에서 추가로 분석하듯이, 이 단계적 접근법은 경험적으로 단일 단계 설정보다 더 안정적인 학습 결과를 낸다. 다양한 입력과 외란 조합에서 target end-effector position x_ee^target 및 base velocity v_base^target을 정확히 추종하면 reward를 부여하여 policy 학습을 지도한다. 또한 robot state와 외력 모두에 대한 state estimator의 정확도를 개선하기 위해 MSE loss를 사용한다. 전체 reward 명세는 [[REF:tab:method:rewards]]에 제시한다.

## Force-aware imitation learning

실제 manipulation task에서 force 정보가 중요하지만 기존 dataset 대부분에는 이 정보가 없다는 점을 고려하여, 학습한 force-position policy를 활용해 imitation learning을 위한 force-aware 데이터를 수집한다. 구체적으로 robot을 teleoperation하여 joint state, base state, control command, 추정된 end-effector contact force, 그리고 end-effector와 robot base 각각에 장착한 camera의 RGB image를 기록한다. 이 데이터는 robot state, 추정 force, image observation을 입력으로 받고 force 명령과 end-effector position 명령을 모두 예측하여 low-level force-position policy의 입력으로 제공하는 diffusion 기반 force-aware imitation learning policy를 학습하는 데 사용한다. 시각 입력에만 의존하는 선행 연구와 달리, 본 force estimator는 policy에 contact 정보를 보충하여 더욱 정확한 object 상호작용과 force 인가를 가능하게 한다. 수집한 데이터의 영향과 본 접근법의 효과는 [[REF:sec:exp:imitation]]에서 검증한다. Teleoperation pipeline과 학습 절차의 세부사항은 각각 [[REF:sec:appendix:teleop_details]]와 [[REF:sec:appendix:il_training_details]]에 제시한다.
