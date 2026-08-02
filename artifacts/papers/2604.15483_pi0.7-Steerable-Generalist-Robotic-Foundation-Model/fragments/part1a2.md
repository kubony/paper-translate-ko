[P1A2-001 | 원문 203–204행]
## 2. 관련 연구

[P1A2-002 | 원문 206–209행]
**범용 로봇 조작 policy.** 범용 로봇 policy 개발을 연구한 방대한 선행 연구가 존재한다. 이러한 범용 policy는 때때로 처음부터 학습되지만, 사전 학습된 vision-language model 또는 사전 학습된 video generation model로 초기화하는 경우가 더 일반적이다. 여러 연구에서는 memory, 장기 계획을 위한 hierarchy, goal image conditioning과 같은 VLA의 아키텍처 구성 요소를 개발했다. 본 연구에서는 π₀.₆-MEM 아키텍처를 기반으로 이 세 구성 요소를 모두 하나의 모델에 통합한 VLA 모델을 개발한다. 범용 policy는 대부분 로봇 시연 데이터로 학습되지만, 선행 연구에서는 웹 데이터, 인간의 egocentric video, 자율 로봇 경험을 pretraining에 포함해 이점을 얻는 방법을 보였다. 본 연구에서는 이러한 데이터 소스를 모두 통합하며, 다양한 데이터와 상세한 prompting을 결합하면 compositional generalization의 강력한 징후와 뛰어난 out-of-the-box 동작을 보이는 모델을 얻을 수 있음을 확인한다.

[P1A2-003 | 원문 211–216행]
**task와 embodiment 전반의 일반화.** 많은 선행 연구는 서로 다른 환경, 객체, 배경뿐 아니라 완전히 새로운 task와 embodiment에도 일반화되는 로봇 policy를 학습하는 것을 목표로 삼았다. 흔히 이를 위해 인간 비디오 데이터를 활용하는데, 일반적인 representation learning에 사용하거나, 인간의 동작으로 직접 supervision하거나, 2D point track을 추출하는 방식이 있다. 다른 연구에서는 학습 또는 inference 중에 인터넷으로 사전 학습된 foundation model을 직접 활용하여 일반화를 개선하고자 했다. 대규모 cross-embodiment 로봇 데이터셋의 가용성이 높아짐에 따라 로봇 간 cross-embodiment transfer를 명시적으로 개선하는 연구도 이루어졌다. 기존 데이터셋을 활용하는 대신, 데이터를 수집한 뒤 다양한 로봇 embodiment에 일반화할 수 있도록 특수한 hand-held device를 제안한 연구도 있다. 본 연구에서는 적절한 prompting을 통해 모델이 다양한 로봇, 인간, 인터넷 데이터를 활용하여 task와 embodiment 전반에서 강력한 일반화를 달성할 수 있음을 확인한다.

[P1A2-004 | 원문 219–221행]
**subgoal image로 로봇 prompting하기.** $\pi_{0.6}\texttt{-MEM}$과 비교할 때 본 모델의 핵심 아키텍처 구성 요소는 생성된 subgoal image를 포함한 goal image를 사용해 모델에 prompt를 제공할 수 있게 한다는 점이다. 로봇 조작 policy를 goal image와 video에 conditioning하는 방식은 방대한 연구에서 탐구되어 왔다. 이들 연구 중 일부는 사용자가 제공한 image를 활용하며, 다른 연구들은 별도 모델이 생성한 goal image 또는 chain-of-thought 방식으로 policy를 conditioning한다. 또 다른 방법으로는 image 및 video generation을 policy 학습 objective에 통합하여 policy representation을 개선하고 더 일반화 가능한 action을 생성할 수 있다. 본 연구의 기여는 이러한 연구들과 상호 보완적이라고 본다. 새로운 아키텍처나 모델 설계를 제안하기보다는 VLA가 더 다양한 데이터 소스를 활용하도록 하는 방법론을 제시하고, 이 방법론이 compositional generalization의 강력한 징후로 이어진다는 실증 분석을 제공하는 데 목적이 있다. 우리가 아는 한, 본 연구의 실증 결과는 선행 연구에서 보고한 정량적 개선을 크게 넘어선다. 세탁물 접기와 같은 정교한 기술이 다른 로봇으로 zero-shot transfer되는 것과 air fryer 조작 같은 새로운 객체 상호작용으로 일반화되는 것을 보여준다.
