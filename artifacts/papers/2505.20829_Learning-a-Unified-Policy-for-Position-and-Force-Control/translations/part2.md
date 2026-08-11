<!-- source: main.tex lines 293-431 -->

# 실험

## Force 및 position 명령 추종

[[FIGURE:fig:unified_experiment|fig/unified_experiment.pdf|\linewidth]]

**Force 및 position control 평가.** (a)–(c) 시뮬레이션 환경에서 force 및 position control 추종 오차를 평가한다. (d) 실제 환경에서 force control을 평가하며, 음영 영역은 서로 다른 5개의 end-effector position에서 측정한 분산을 나타낸다.

**Position 추종.** 시뮬레이션에서의 성능을 평가하기 위해, 전체 학습 workspace를 포괄하도록 position 명령만으로 무작위 생성한 end-effector trajectory를 사용하여 6000-step rollout을 수행한다. 이 trial들에 걸친 평균 position 추종 오차와 추정 오차를 보고한다. [[REF:fig:unified_experiment]](b)에 나타난 바와 같이, 외력과 force 명령이 없을 때 end-effector 추종 오차는 대부분 0.1m 이내로 유지된다. Y축에서는 오차가 약간 더 크게 관찰되는데, 이는 해당 방향에서 사용할 수 있는 자유도가 더 적어 정밀도가 제한되기 때문인 것으로 보인다. 또한 추정된 end-effector position을 시뮬레이션의 ground-truth 값과 비교하여 상태 추정기의 정확도를 평가한다. [[REF:fig:unified_experiment]](a)에 나타난 바와 같이, 모든 축에서 추정 오차는 0.05m 이내로 유지된다.

**Force control.** 두 가지 설정에서 제안한 policy가 force를 추정하고 force에 따라 동작하는 능력을 평가한다. 먼저 policy가 가해진 외력과 일치하는 force 명령을 받을 때 position 추종 성능을 평가하며, 이를 통합 force-position control을 평가하기 위한 간접 평가로 사용한다. [[REF:fig:unified_experiment]](c)에 나타난 바와 같이, 외력이 없는 실험과 비교하면 추종 오차가 force가 없는 설정보다 약간 증가하지만 대부분 0.1m 이내로 유지되어, 효과적인 force-aware 동작을 입증한다. 둘째, 0 N부터 60 N까지의 force 명령을 가하고 동력계를 사용해 end-effector force를 측정함으로써 실제 로봇에서 직접적인 force control 평가를 수행한다. 서로 다른 5개의 end-effector position에서 측정한 결과, [[REF:fig:unified_experiment]](d)에 나타난 바와 같이 평균 오차는 10 N 이내이다. 6개의 이산적인 force 수준에 대한 force 추정에서는 5–10 N의 오차가 나타난다. 하드웨어 한계로 인해 Y축과 Z축에 대한 평가는 40 N으로 제한한다. 특히 Y축에서 경미한 sim-to-real 불일치가 존재함에도, 추정기는 대상 manipulation task에 충분한 정확도를 유지한다. 더 자세한 분석은 [[REF:sec:appendix:real_word_force_control_experiment]]에서 제공한다.

## Force-aware 모방학습

**Task 설정.** Hybrid force-position control과 force sensing이 필요한 네 가지 실제 task인 `wipe-blackboard`, `open-cabinet`, `close-cabinet`, `open-drawer-occlusion`에서 본 방법을 평가한다. `wipe-blackboard` task에서 로봇은 잉크 자국을 지우기 위해 표면과 지속적으로 contact를 유지하면서 측면으로 움직여야 한다. 50개의 trajectory를 수집하고 force-aware diffusion policy를 30k step 동안 학습한다. `open-cabinet`과 `close-cabinet`에서는 로봇이 눌러서 여는 캐비닛과 상호작용하며, `open-drawer-occlusion`에서는 시각 관측에서 점차 가려지는 서랍을 연다(설정은 [[REF:fig:open_drawer]] 참조). 세 가지 열기/닫기 task 각각에 대해 task당 30개의 episode를 수집하고 policy를 20k step 동안 학습한다.

Baseline으로 학습된 low-level policy를 배포하되, teleoperation 데이터 수집 중에는 force 추정기와 force 명령 신호를 제외한다. 각 task는 50회 수행하며, 성공적인 완료를 위해 각 trial은 최대 1000 step($\sim$20\ seconds)으로 제한한다. 완전성을 위해 task 정의와 실험 설정에 관한 추가 세부사항을 [[REF:sec:appendix:il_training_details]]에 제공한다.

[[FIGURE:fig:imitation|fig/exp_il.pdf|0.95\linewidth]]

**Force-aware 모방학습.** (a) `wipe-blackboard` task에서 학습된 force-aware imitation policy가 출력하는 position 및 force 명령의 시계열이다. *cmd*는 imitation learning policy의 출력을 나타내고, *pred*는 low-level policy가 추정한 외력을 나타낸다. (b) 데이터 수집 과정을 시각화한다. (c) 네 가지 task에 걸쳐 50회의 trial에서 본 policy와 vision-only baseline policy의 성능을 비교한다.

**결과 및 분석.** [[REF:fig:imitation]]에서 네 가지 실제 task에 대해 본 방법을 baseline과 비교한다. 본 접근법은 baseline보다 $\sim$39.5\% 더 높은 성공률을 달성한다.

`wipe-blackboard`에서 position-only policy는 안정적인 contact를 유지하지 못하며, 그 결과 닦기가 불충분하거나 과도한 force로 인해 표면이 손상될 위험이 자주 발생한다. 반면 본 force-aware policy는 일관된 contact pressure를 보장하며, low-level policy는 compliance를 향상하고 기계적 stress를 줄인다.

`open-` 및 `close-cabinet`에서 주된 과제는 눌러서 여는 메커니즘의 좁은 3mm stroke에 있으며, 이는 vision만으로 감지하기 어렵다. 본 force 추정기는 필요한 contact force를 정확히 감지하여 메커니즘을 안정적으로 작동시킨다. `open-drawer-occlusion`에서 시각 단서에만 의존하는 baseline policy는 관측할 수 없는 contact로 인해 성공률이 0.3까지 급격히 하락한다. 본 방법은 force sensing을 활용하여 가림 상황에서 contact를 감지함으로써 성공률을 0.76으로 높이며, vision이 제한된 상황에서 force 추정의 중요성을 부각한다. 모든 정량적 비교와 추가 세부사항은 [[REF:sec:appendix:il_training_details]]에 제공한다.

## 기본 manipulation policy

**Force control.** Force control은 가해진 force와 명령 force가 일치할 때까지 end-effector를 force 방향으로 움직여 명령된 force를 직접 가한다. 본 통합 전략은 추가 학습을 필요로 하지 않으며, [[REF:eq:force_control]]에 따라 추정된 외력과 force 명령의 합이 평형에 도달할 때까지 변위 보상을 결정한다. [[REF:fig:skills]](a)와 supplementary video에 나타난 바와 같이, $2.5 kg$ dumbbell을 end-effector에 부착하면 로봇은 $25 N$의 상향 force 명령으로 균형을 달성한다. 그러나 이 명령이 없으면 dumbbell의 중력으로 인해 end-effector가 내려간다.

[[FIGURE:fig:skills|fig/demo_v5.pdf|\linewidth]]

**본 policy로 구현되는 다양한 skill.** (a) Force control: $25N$의 force 명령이 주어지면 로봇이 중력에 대응하여 payload를 지지한다. (d) Base force 추종: 로봇이 base에 가해지는 밀기에 compliant하게 반응하여 직관적인 인간의 유도를 가능하게 한다. (c) Force 추종: 로봇이 외력 상호작용을 최소화하여 zero-force 명령을 추종한다. (d) Impedance control: 로봇이 외란에 대응하고 compliant하게 반응하도록 whole-body 자세를 조정한다.

**Force 추종.** Force 추종은 end-effector가 zero-force 명령을 추종하는 force control의 특수한 경우이다. 외력이 가해지면 end-effector는 force 방향으로 움직인다. Force가 제거되면 원래 target으로 돌아가는 대신 이동한 position에 머문다. 이 동작은 [[REF:eq:force_tracking]]에 따라 본 통합 policy를 사용하여 구현한다. [[REF:fig:skills]](c)와 supplementary video에 나타난 바와 같이, force 명령을 0으로 설정하여 이 기능을 시연한다. 이 경우 end-effector는 외력을 따라 움직이고 force가 제거된 후에도 이동한 position에 남아 효과적인 force 추종을 달성한다.

**Impedance control.** Force control의 핵심 응용 중 하나는 impedance control이며, 이때 end-effector는 spring-mass-damper system의 dynamics를 따르면서 외력에 compliant하게 반응하는 동시에 target position을 추종한다. [[REF:eq:impedance_control]]에 따라 통합 policy를 사용해 impedance control을 구현한다. [[REF:fig:skills]](d)와 supplementary video에 나타난 바와 같이, 인간-로봇 줄다리기와 팔씨름 상황에서 이 기능을 시연한다. 이 task들에서는 end-effector가 target position에서 더 멀리 벗어날수록 로봇이 가하는 저항력이 더 커져 impedance 동작을 보여준다.

## 서로 다른 embodiment에서의 성능

통합 policy의 cross-embodiment 능력을 검증하기 위해 Unitree G1 humanoid robot과 Unitree B2-Z1 quadrupedal manipulator에서 이를 시험한다. Locomotion의 경우 force 보상이 end-effector에 직접 적용되는 manipulation task와 달리, [[REF:eq:base_pos_force]]에 따라 외력을 보상하도록 로봇의 base velocity를 조정한다.

[[REF:fig:teaser]]의 세 번째 행에 나타난 바와 같이, 보상 velocity의 크기가 velocity 명령과 같고 방향이 반대이면 humanoid robot은 멈추고 균형을 유지하기 위해 몸을 기울인다. 마찬가지로 [[REF:fig:skills]](b)에 나타난 바와 같이, quadrupedal robot은 force와 velocity 명령이 모두 0인 상태에서도 발로 차이면 앞으로 걷기 시작한다.

# 결론

Legged robot을 위한 통합 force-position control policy를 제안하며, 이를 통해 명시적인 force sensor 없이 contact-rich loco-manipulation task를 수행할 수 있다. 본 policy는 reinforcement learning을 사용하여 과거 state로부터 외력을 추정하고 position 및 velocity 조정을 통해 이를 보상한다. 이 접근법은 position 추종, force 인가, compliance와 같은 다양한 동작을 지원한다. 또한 force 추정을 imitation learning에 통합하면 contact-rich 환경에서 task 성공률이 향상된다. Quadrupedal robot과 humanoid robot에서 수행한 실험은 실제 환경에서 policy의 적응성과 강건성을 검증한다.

# 한계 및 향후 연구

첫째, policy는 직접적인 force sensing 없이 외력을 성공적으로 추정하지만, 고주파 상호작용과 로봇 workspace의 경계에서는 정확도가 저하되는 경향이 있다. 향후 연구에서는 이러한 corner case에서 force 추정을 개선하는 데 초점을 맞출 수 있다. 가능한 한 가지 방향은 [[REF:eq:pos_force_target]]의 velocity 및 acceleration 항을 통합하여 force 추정을 향상하는 것이며, 이를 통해 모델이 동적 상호작용을 더 잘 포착하도록 할 수 있다.

둘째, 본 policy는 시뮬레이션에서 실제 환경 배포로 잘 일반화되지만, 특히 서로 다른 좌표축에서의 force 정확도와 관련하여 sim-to-real gap으로 인한 불일치가 남아 있다. 이러한 차이는 시뮬레이션과 실제 하드웨어 간 actuator dynamics 및 contact modeling의 불일치에서 비롯된 것으로 보인다. 향후 연구에서는 다양한 실제 조건 전반에서 강건성을 향상하기 위해 domain randomization 및 real-to-sim correction과 같은 기법을 탐구할 수 있다.

또한 현재 framework는 주로 단일 상호작용 지점에서 force를 추정하는 데 초점을 맞춘다. 향후 연구에서는 다중 지점 force 추정과 whole-body force 상호작용 task를 탐구할 수 있다. 예를 들어 quadrupedal robot이 무거운 문을 여는 상황에서 로봇은 몸으로 문을 받치는 동시에 manipulator를 사용하여 손잡이를 아래로 누를 수 있다. 서로 다른 신체 부위에 걸친 여러 contact force를 조정하는 policy를 개발하면 더 복잡하고 효과적인 실제 상호작용이 가능해질 수 있다.
