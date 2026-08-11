<!-- source: main.tex lines 462-556 -->

# 문제 정식화

본 policy는 다양한 force 및 position 입력에서 position control, force control, impedance control, hybrid position-force control을 포함한 폭넓은 manipulation 동작을 가능하게 한다. [[REF:eq:pos_force_target]]의 정식화로부터 다음과 같은 기본 manipulation policy를 쉽게 유도할 수 있다.

- ***a) Position control:*** 외부 외란이나 능동 force 명령이 가해지지 않을 때 [[REF:eq:pos_force_target]]은 다음과 같이 된다.

  $$
  \mathbf{x}^{\mathrm{target}} = \mathbf{x}^{\mathrm{cmd}}.
  $$

  [[REF:eq:pos_control]]

  여기서 target end-effector position $\mathbf{x}^{\mathrm{target}}$은 명령된 position $\mathbf{x}^{\mathrm{cmd}}$에 도달해야 한다.

- ***b) Force control:*** 환경과 contact한 상태에서 외부 외란 없이 force $\mathbf{F}^{\mathrm{cmd}}$를 가할 때, end-effector의 desired goal position은 [[REF:eq:pos_force_target]]에 따라 다음과 같이 정의된다.

  $$
  \mathbf{x}^{\mathrm{target}} = \mathbf{x}^{\mathrm{cmd}} + \frac{\left(\mathbf{F}^{\mathrm{cmd}} - \mathbf{F}^{\mathrm{react}}\right)}{K}.
  $$

  [[REF:eq:force_control]]

  시스템 실행 중 reaction force $\mathbf{F}^{\mathrm{react}}$는 force 명령 $\mathbf{F}^{\mathrm{cmd}}$과 일치할 때까지 점진적으로 증가하며, 최종 target pose는 $\mathbf{x}^{\mathrm{target}}_{\mathrm{final}} = \mathbf{x}^{\mathrm{cmd}}$가 된다.

- ***c) Impedance control:*** end-effector가 외부 외란 force를 받지만 환경에는 force를 가하지 않을 때 [[REF:eq:pos_force_target]]은 다음과 같이 단순화된다.

  $$
  \mathbf{x}^{\mathrm{target}} = \mathbf{x}^{\mathrm{cmd}} + \frac{\mathbf{F}^{\mathrm{ext}}}{K}.
  $$

  [[REF:eq:impedance_control]]

  여기서 end-effector는 외부 외란을 받을 때 position을 조정하여 외력 $\mathbf{F}^{\mathrm{ext}}$에 대해 compliance를 나타낸다. 특히 다음과 같이 position 명령 $\mathbf{x}^{\mathrm{cmd}}$을 동적으로 조정함으로써 [[REF:eq:impedance_control]]을 사용해 force 추종과 중력 보상도 구현할 수 있다.

  $$
  \Delta \mathbf{x}^{\mathrm{cmd}} = \frac{\mathbf{F}^{\mathrm{ext}}}{K}.
  $$

  [[REF:eq:force_tracking]]

  여기서 $\mathbf{F}^{\mathrm{ext}}$는 중력 항 또는 외력일 수 있다.

- ***d) Hybrid position-force control:*** [[CITE:raibert1981hybrid]]에서 정의한 바와 같이, hybrid position-force control은 $\mathbf{x}^{\mathrm{cmd}}$을 사용해 end-effector의 움직임을 제어하는 동시에 움직임의 접선 방향에 수직인 force 명령 $\mathbf{F}^{\mathrm{cmd}} = \mathbf{F}^{\mathrm{cmd}}_{\perp}$를 가하는 것을 의미한다. 이 시나리오에서 시스템은 force 명령이 없는 접선 방향을 따라 [[REF:eq:pos_control]]을 따르고, force 명령이 활성화된 수직 방향에서는 [[REF:eq:force_control]]을 만족한다.

**단순화된 impedance 모델.** 본 정식화에서는 damping 항과 inertia 항을 생략한다. 이러한 단순화는 움직임이 느리고 normal force가 contact를 보장하는 비교적 정적인 또는 준정적인 task(예: 닦기 또는 줄다리기)에 적합하다. 이러한 경우에는 정적 모델로 충분하다. 동적이거나 민첩한 skill에는 더 높은 control 주파수와 명시적인 velocity/acceleration 항이 필요하며, 향후 연구에서 이를 탐구할 계획이다.

**Rigid contact 가정.** 본 정식화 $\mathbf{F} = K(\mathbf{x} - \mathbf{x}^{\mathrm{des}})$은 rigid object와 compliant object를 모두 자연스럽게 처리한다. 이는 물체의 stiffness와 무관하게 end-effector position이 net force $\mathbf{F}$와 desired goal position $\mathbf{x}^{\mathrm{des}}$에만 의존하기 때문이다. Rigid contact에서는 작은 변위가 필요한 force를 생성하는 반면, soft object에서는 force 평형에 도달할 때까지 더 큰 변형이 발생한다.

# 하드웨어 설정 및 Teleoperation 시스템

[[FIGURE:fig:b2z1_hardware|fig/hardware.pdf|0.48\linewidth]]

**B2-Z1 로봇 하드웨어.** Z1 arm이 장착된 Unitree B2 로봇을 wireless controller를 통해 teleoperation하며, 시각 입력에는 두 대의 RealSense camera를 사용한다.

[[FIGURE:fig:iphone_tele|fig/iphone_tele.jpg|0.48\linewidth]]

**iPhone teleoperation.** MuJoCo AR 앱을 사용하여 iPhone으로 manipulation task를 수행하는 로봇을 원격 제어한다.

**하드웨어 설정 및 teleoperation 시스템.** [[REF:fig:hardware]]

**로봇 시스템 설정.** Humanoid robot 시스템([[REF:fig:method:model]])은 29-DOF Unitree G1 로봇이다. Quadruped robot 시스템([[REF:fig:b2z1_hardware]])은 12-DOF Unitree B2 로봇과 6-DOF Unitree Z1 robot arm으로 구성되며, 둘 다 B2의 battery로 구동된다. Quadruped robot의 arm과 head에 장착한 두 대의 RealSense camera를 맞춤 구성한다. 본 whole-body controller와 diffusion policy 추론은 RTX 3090 GPU가 탑재된 전용 desktop에서 실행되며, internet 연결을 통해 B2-Z1 로봇과 interface한다.

**Teleoperation 시스템.** [[REF:fig:iphone_tele]]에 나타난 바와 같이, position control만 필요한 manipulation task에는 iPhone을 사용해 로봇을 유연하게 teleoperation할 수 있는 MuJoCo AR 애플리케이션을 활용한다. 그러나 [[REF:fig:b2z1_hardware]]에 나타난 바와 같이 이 접근법은 hybrid force-position control이 수반되는 manipulation task에는 더 이상 적합하지 않다. 이를 해결하기 위해 B2 로봇의 내장 wireless controller에 기반한 전용 teleoperation 시스템을 개발했다. 이 시스템에서는 두 개의 joystick으로 로봇의 base 움직임을 제어하고, 아래쪽의 버튼 여덟 개를 end-effector position과 gripper의 열림/닫힘 제어에 매핑한다. 또한 “L1” 버튼을 누르고 있으면 시스템이 end-effector에 position 명령을 내리는 모드에서 force 명령을 내리는 모드로 전환된다.

실제로 이 설정을 사용한 데이터 수집은 주로 teleoperation의 제한된 bandwidth 때문에 비교적 느렸으며, 예를 들어 닦기 trial당 약 20초, 캐비닛 trial당 약 10초가 걸렸다. Force feedback을 제공하는 exoskeleton 기반 teleoperation이 forceful manipulation을 위한 demonstration을 수집하는 데 더 자연스럽고 효율적인 방법을 제공할 것으로 보며, 향후 연구에서 이 방향을 탐구할 계획이다.

# Reinforcement learning을 사용한 Policy 학습의 세부사항

Actor policy를 학습하기 위해 PPO [[CITE:schulman2017proximal]]를 사용하고, state prediction 출력을 위한 MLP network로 state estimator를 구현한다. 4096개의 병렬 환경을 갖춘 Isaac Gym [[CITE:makoviychuk2021isaac]]에서 RL policy를 학습한다.

## 입력 명령 및 외란 Force

학습 중에는 아래 범위 내에서 입력 명령과 외란 force를 sampling한다.

1. Body frame 내 구면좌표계의 end-effector position 명령

   $\mathbf{x}^{\mathrm{cmd}}_{\mathrm{ee}} = \left(r^{\mathrm{cmd}}, \theta^{\mathrm{cmd}}, \phi^{\mathrm{cmd}}\right)$이며, 각 범위는 다음과 같다.

   $r^{\mathrm{cmd}} \in [0.35, 0.85\,\mathrm{m}]$,

   $\theta^{\mathrm{cmd}} \in [-0.4\pi, 0.4\pi\,\mathrm{rad}]$,

   $\phi^{\mathrm{cmd}} \in [-0.6\pi, 0.6\pi\,\mathrm{rad}]$.

2. Body frame 내 데카르트 좌표계의 end-effector force 명령

   $\mathbf{F}^{\mathrm{cmd}}_{\mathrm{ee}} \in \mathbb{R}^{3}$: $[-60\,\mathrm{N}, 60\,\mathrm{N}]$.

3. Base velocity 명령 $\mathbf{v}^{\mathrm{cmd}}_{\mathrm{base}} = \left(v^{\mathrm{cmd}}_x, v^{\mathrm{cmd}}_y, \omega^{\mathrm{cmd}}_z\right)$이며, 각 범위는 다음과 같다.

   $v_x \in [-0.8, 0.8\,\mathrm{m/s}]$,

   $v_y \in [-0.6, 0.6\,\mathrm{m/s}]$,

   $\omega_z \in [-0.8, 0.8\,\mathrm{rad/s}]$.

4. Body frame 내 base force 명령

   $\mathbf{F}^{\mathrm{cmd}}_{\mathrm{base}} \in \mathbb{R}^{3}$: $[-60\,\mathrm{N}, 60\,\mathrm{N}]$.

5. 환경이 end-effector에 가하는 외부 net force

   $\mathbf{F}_{\mathrm{ee}} \in \mathbb{R}^{3}$: $[-60\,\mathrm{N}, 60\,\mathrm{N}]$이며, robot base에서는 $\mathbf{F}_{\mathrm{base}} \in \mathbb{R}^{3}$: $[-60\,\mathrm{N}, 60\,\mathrm{N}]$이다.
