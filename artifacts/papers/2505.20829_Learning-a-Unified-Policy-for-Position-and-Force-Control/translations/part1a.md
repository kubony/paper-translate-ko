source: main.tex active lines 99-180

## 초록

로봇 loco-manipulation에는 환경과의 contact-rich 상호작용이 수반되는 경우가 많으며, 이를 위해서는 contact force와 로봇 position을 함께 모델링해야 한다. 그러나 최근의 시각운동 policy는 position control 또는 force control 중 하나만 학습하는 데 초점을 맞추는 경우가 많아, 이 둘의 공동 학습을 간과한다. 본 연구에서는 force 센서에 의존하지 않고 학습한 force 및 position control을 공동으로 모델링하는, 다족 로봇을 위한 최초의 통합 policy를 제안한다. 다양한 position 및 force 명령 조합을 외부 교란 force와 함께 시뮬레이션함으로써, 과거 로봇 상태로부터 force를 추정하고 position 및 속도 조정을 통해 이를 보상하는 policy를 강화학습으로 학습한다. 이 policy는 다양한 force 및 position 입력하에서 position tracking, force 인가, force tracking, compliant 상호작용을 포함한 광범위한 manipulation 행동을 가능하게 한다. 또한 학습한 policy가 force 추정 모듈을 통해 필수적인 contact 정보를 통합함으로써 trajectory 기반 모방학습 파이프라인을 향상시키며, 네 가지 까다로운 contact-rich manipulation 과제에서 position-control policy보다 성공률이 약 39.5% 더 높음을 보인다. 사족보행 manipulator와 휴머노이드 로봇 모두에서 수행한 실험을 통해 다양한 시나리오에서 제안한 policy의 범용성과 강건성을 검증한다.

**키워드:** 통합 Force 및 Position Control, Force-aware 모방학습

## 1. 서론

다족 로봇은 최근 locomotion과 manipulation에서 발전을 이루어 [[CITE:hwangbo2019learning,zhuang2024humanoid,he2024agile,hoeller2024anymal]], 복잡한 지형(예: 계단)을 횡단하고 적응형 신체 자세를 통해 작업공간을 확장할 수 있게 되었으며, 이에 따라 loco-manipulation에 대한 관심이 다시 높아졌다 [[CITE:sleiman2023versatile,fu2023deep,liu2024visual,qiu2024wildlma]]. 그러나 다족 manipulator는 복잡한 운동학적 구조로 인해 제어하기 어렵다. contact-rich manipulation 과제에서는 원하는 제어 행동(예: compliance)에 contact force의 정확한 모델링이 필수적이지만 force 감지 하드웨어가 없어 이를 수행하기 어렵기 때문에, 이러한 난점은 더욱 심해진다. 이와 같은 과제는 효과적인 로봇-환경 및 인간-로봇 상호작용을 지원하기 위한 강건하고 적응 가능한 policy의 필요성을 부각한다.

다족 manipulator의 제어 문제를 해결하기 위해 강화학습 알고리즘은 전통적 제어 방법의 효과적인 대안으로 부상했으며, domain randomization을 통해 학습된 강건하고 일반화 가능한 policy를 제공한다 [[CITE:fu2023deep,liu2024visual,qiu2024wildlma,portela2024learning,zhuang2024humanoid,zhuang2023robot]]. 이러한 policy는 복잡한 과제에서 locomotion과 manipulation을 통합하지만, 주로 정밀한 position control에 의존하므로 contact-rich 시나리오에 적용하는 데 한계가 있다. 이러한 의존성은 position 기반 로봇 모방학습의 부상도 촉진했으며 [[CITE:shridhar2023perceiver,chi2023diffusion,brohan2023rt,team2024octo,black2024pi_0]], 대규모 데이터셋 [[CITE:walke2023bridgedata,brohan2023rt,khazatsky2024droid,o2024open]]은 로봇 trajectory에만 초점을 맞추고 force 감지가 없다는 이유로 중요한 contact 정보를 누락한다. [[REF:sec:exp:imitation]]에서 보이듯, 이처럼 trajectory만으로 이루어진 데이터는 기본적인 contact-rich 과제(예: 칠판 닦기)에서조차 효과적인 policy를 학습하기에 불충분하다. 이는 position control의 한계를 드러내며, 더 효과적인 과제 수행을 위해 학습 기반 policy에 force 감지와 모델링을 통합해야 할 필요성을 강조한다.

앞서 언급한 과제와 관찰에 비추어, 본 연구에서는 **force 센서 없이 force 및 position control을 매끄럽게 통합하는 다족 로봇용 최초의 통합 policy**를 제안한다. force 및 position control을 독립적으로 처리하는 기존 방법 [[CITE:portela2024learning]]과 달리, 본 연구에서는 다양한 position 및 force 명령 조합을 외부 교란 force와 함께 시뮬레이션하여 Isaac Gym [[CITE:makoviychuk2021isaac]]에서 강화학습으로 단일 제어 policy를 학습한다. 이 policy는 force 추정기를 활용하여 로봇의 과거 상태와 목표 position에 대한 offset을 바탕으로 외부 force를 예측함으로써, 로봇의 position과 속도를 적응적으로 조정할 수 있게 한다. 학습한 policy는 다양한 force 및 position 입력에 대한 position tracking, force 인가, force tracking, compliant 응답을 포함하는 다채로운 manipulation 행동을 지원한다. 또한 Unitree B2-Z1 사족보행 manipulator 플랫폼과 Unitree G1 휴머노이드 로봇 모두에서 7개 과제에 걸친 광범위한 실험을 수행하여, 이 학습 프레임워크가 서로 다른 로봇 embodiment에 일반화될 수 있음을 검증한다.

아울러 학습한 policy가 contact force 정보를 포함한 모방학습을 촉진하는 역량을 부각한다. 구체적으로, 학습한 policy를 기본 원격조작 policy로 활용하여 position 및 force 명령을 로봇에 동시에 전달하는 한편, 내장된 contact force 추정기를 통해 contact-rich manipulation 데이터를 수집하는 force-aware 데이터 수집 파이프라인을 개발한다. 추정 force를 position 기반 모방학습 policy에 통합하여 이 데이터의 효과를 검증하며, 그 결과 세 가지 까다로운 contact-rich 과제 전반에서 **기본 position 기반 방법보다 성공률이 크게 향상(약 39.5%)**된다. 이러한 실험 결과는 특히 명시적인 force 센서가 없는 상황에서, 학습한 policy가 contact-rich 로봇 상호작용 데이터를 구축하기 위한 범용 프레임워크로 활용될 잠재력을 강조한다.

전반적인 기여는 다음과 같이 요약할 수 있다.

1. 다족 loco-manipulation에서 통합 force 및 position control을 학습하는 최초의 모델을 제안하며, 단일 policy로 position tracking, force control, compliance와 같은 다양한 제어 행동을 가능하게 한다.
2. 사족보행 manipulator와 휴머노이드 로봇에서 수행한 7개 실험을 통해, 다양하고 까다로운 과제 시나리오 전반에서 학습한 policy의 효과와 강건성을 입증한다.
3. 학습한 force 추정기를 사용하는 force-aware 로봇 모방학습 데이터 수집 파이프라인을 개발하여, 세 가지 까다로운 contact-rich manipulation 과제에서 position 기반 모방학습 baseline을 약 39.5% 향상시킨다. 이는 contact-rich 과제 시연 데이터를 구축하기 위한 범용적이고 효율적인 프레임워크로서 본 policy가 지닌 가능성을 보여준다.

## 2. 관련 연구

### Whole-body Control

Whole-body control은 특히 고전적 제어 프레임워크 내에서 mobile manipulation의 로봇 역량을 향상하기 위해 널리 채택되어 왔다 [[CITE:sleiman2021unified,polverini2020multi,sleiman2023versatile]]. 최근에는 병렬 시뮬레이터를 사용하는 강화학습 [[CITE:makoviychuk2021isaac,rudin2022learning]]이 다족 로봇의 복잡한 제어 문제를 해결하는 주류 접근법이 되었다. 여러 학습 기반 방법 [[CITE:fu2023deep,pan2024roboduet,ma2022combining,liu2024visual,wang2024quadwbg]]은 whole-body control의 강건성을 향상했으며, 다른 연구들은 이를 force 집약적 과제로 확장했다 [[CITE:murphy2012high,murooka2015whole,rehman2016towards,bellicoso2019alma,risiglione2022whole]]. 예를 들어, [[CITE:murooka2015whole]]는 밀기 과정에서 충분한 force를 인가하도록 관절 움직임을 조정하며, ALMA [[CITE:bellicoso2019alma]]는 whole-body control과 force control을 결합하여 정밀한 end-effector 구동을 달성한다. [[CITE:risiglione2022whole]]는 Cartesian impedance control을 QP 정식화에 통합하여, 이중 질량-댐퍼-스프링 모델을 통해 compliant loco-manipulation을 가능하게 한다. 이 연구들은 전체적으로 force 및 position control을 통합하는 whole-body control의 효과를 보여준다.

### Hybrid Force 및 Position Control

contact-rich manipulation 과제에서는 force와 position 사이의 본질적인 결합으로 인해 end-effector trajectory control에만 의존하는 것으로는 충분하지 않은 경우가 많다. impedance control의 도입 [[CITE:hogan1984impedance]]을 포함한 초기 연구 [[CITE:raibert1981hybrid,mason1981compliance,yoshikawa1987dynamic,hogan1984impedance]]는 hybrid force-position 전략의 토대를 마련했다. 최근 연구 [[CITE:hwangbo2019learning,zhang2021learning,hou2024adaptive,de2024current,portela2024learning]]는 compliance control을 발전시켰으며, 일부는 force 센서를 활용하고 다른 일부는 내부 신호나 강화학습을 통해 force를 간접적으로 추정한다. 이러한 흐름에서 영감을 받아, 본 연구는 강화학습으로 사족보행 로봇이 force와 position을 동시에 제어하도록 학습함으로써 force 센서의 필요성을 제거한다. 이는 서로 다른 명령 구성을 통해 force following, impedance control, hybrid 모드 사이를 유연하게 전환할 수 있게 한다.

### Mobile Manipulation을 위한 모방학습

모방학습 [[CITE:bousmalis2023robocat,mees2024octo,vuong2023open,yang2023polybot,fang2024rh20t]]은 최근 로봇이 다양한 과제를 수행하도록 학습시키는 주요 접근법이 되었다. 행동 복제 [[CITE:pomerleau1988alvinn,bojarski2016endendlearningselfdriving]]는 전문가 시연의 관측-action 쌍을 지도학습하여 policy를 학습하는 간명한 모방학습 방법이다. 이미지 데이터와 고유수용성 감지 [[CITE:fu2024mobile,ha2024umi,he2024learning,qiu2024wildlma]]를 활용하여 로봇 제어 명령을 생성하는 연구들은 mobile manipulation 과제에서 괄목할 성공을 보였다. 더 나아가 최근 연구 [[CITE:lin2024learning,yang2023seq2seq]]는 로봇의 감각 역량을 향상하기 위해 촉각 감지를 통합하기 시작했다. 이와 마찬가지로 본 연구는 force 센서에 의존하지 않고 force 입력을 활용하며, 로봇이 까다로운 과제를 효과적으로 완수하도록 하는 데 force 정보가 핵심적임을 보인다.

## 3. 방법

### 3.1 Force 및 Position Control을 위한 통합 정식화

먼저 본 접근법의 일반적인 문제 정식화를 소개한다. [[REF:fig:method:model]](c)의 상단에 보인 것처럼, 로봇 body frame에 상대적인 position 명령과 force 명령 𝐱^cmd 및 𝐅^cmd가 주어졌을 때, 본 연구의 목표는 순 force 𝐅가 작용하는 상황에서 로봇의 행동이 이러한 명령을 따르도록 보장하는 강화학습 policy를 학습하는 것이다.

이 목표를 달성하기 위해 다음의 impedance control 정식화를 채택한다.

𝐅 = K(𝐱 − 𝐱^des) + D(ẋ − ẋ^des) + M(ẍ − ẍ^des).  [[REF:eq:impedance_general]]

여기서 𝐱는 로봇의 실제 position을 나타낸다. 𝐱^des, ẋ^des, ẍ^des는 각각 로봇의 원하는 목표 position, 속도, 가속도를 나타낸다. 매개변수 K, D, M은 각각 강성 계수, 감쇠 계수, 등가 질량(관성)에 해당한다.

#### End-effector 모델링

manipulation 과제에서 end-effector는 일반적으로 느리게 이동하므로, [[REF:eq:impedance_general]]을 다음과 같이 단순화할 수 있다.

𝐅 = K(𝐱 − 𝐱^des).

순 force 𝐅는 주로 세 가지 성분, 즉 능동 force 𝐅^cmd, 𝐅^cmd를 환경에 인가함으로써 발생하는 수동 반력 𝐅^react, 그리고 추가적인 외부 교란 𝐅^ext로 구성된다. 따라서 end-effector의 원하는 목표 position 𝐱^target은 다음과 같이 주어진다.

𝐱^target = 𝐱^cmd + [𝐅^ext + (𝐅^cmd − 𝐅^react)] / K.  [[REF:eq:pos_force_target]]

여기서 환경의 반력은 end-effector가 명령된 position 𝐱^cmd에 도달하지 못하게 한다. [[REF:eq:pos_force_target]]의 정식화에서는 position 명령 𝐱^cmd와 force 명령 𝐅^cmd를 적절히 지정함으로써 *Position Control*, *Force Control*, *Impedance Control*, *Hybrid Position and Force Control*을 포함한 여러 manipulation 행동을 도출할 수 있다. 이러한 제어 행동의 상세한 정식화는 [[REF:sec:appendix:formulation]]에 제시한다. position 명령, force 명령, 외부 교란이 동시에 존재하는 복잡한 시나리오에서 시스템은 [[REF:eq:pos_force_target]]을 따르며, 이러한 기본 제어 모드를 통합한다.
