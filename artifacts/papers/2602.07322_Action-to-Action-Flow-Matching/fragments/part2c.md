## 일반화 성능

### 시각적 불확실성

다양한 시각적 불확실성하에서 제안한 A2A policy의 일반화 성능을 추가로 평가한다. 채택한 플랫폼인 *Roboverse* [[CITE:geng2025roboverse]]는 *Close Box* task의 장면 무작위화를 난이도가 점진적으로 높아지는 네 수준으로 분류한다. Level 0은 학습 데이터셋으로 사용되며 초기 상자 pose 변화를 포함한다(부록 그림 [[XREF:level0]] 참조). Level 1은 상당한 배경 texture 무작위화를 도입하며(부록 그림 [[XREF:level1]] 참조), Level 2는 조명 교란을 추가한다. 마지막으로 Level 3은 카메라 viewpoint 변화를 포함한다. 자세한 무작위화 설정은 부록 [[XREF:appen_dr]]에 제시한다.

[[FIGURE:FIGinitial]]

**서로 다른 초기화에 대한 일반화 시험.** **왼쪽:** 다양한 수준의 초기 상태 불확실성에서의 성공률. 설정: *Close Box*, 30 epochs, 시연 수 100. Noised A2A(N-A2A)는 초기 action 분포에 0.1 STD의 *Gaussian* noise를 적용한 것을 의미한다. **오른쪽:** 다양한 초기 noise 수준에서의 성공률. 초기 상태 불확실성은 0.08 rad로 설정한다.

표 [[XREF:tab-generalization]]은 Level 0부터 3까지 평가한 방법들의 성공률을 제시한다. 특히 Level 1–3을 처음 접하는 경우에도 A2A(6 steps)는 30–40%의 견고한 성공률을 유지하며 모든 baseline 방법을 일관되게 능가한다. 단일 step 추론 regime에서도 A2A는 다른 알고리즘보다 우수한 일반화 성능을 계속 보인다. 그림 [[XREF:real_test]]과 같이 실제 환경 시험에서도 시각적 일반화 성능을 검증했다. 목표 cube를 이전에 보지 못한 발광 변형으로 대체하여 심각한 시각적 distractor를 유발한다. 이 경우 baseline들은 완전히 실패하지만, 본 알고리즘은 견고한 80%의 성공률을 유지한다.

이러한 견고성의 근본 원인은 *representation entanglement* 문제를 완화하는 본 연구의 decoupled 전략에 있다고 주장한다 [[CITE:li2026causal]]. proprioceptive feature와 시각 feature를 단순히 이어 붙이는 기존 방법과 달리, 본 연구는 이들을 서로 다른 전략으로 처리하여 저차원 proprioceptive signal이 고차원 signal에 가려지는 것을 방지하고, 그 결과 모델이 각 modality의 상호 보완적인 강점을 더 효과적으로 활용할 수 있게 한다. 구체적으로, 생성 과정을 과거 action에 grounding하면 시간에 따른 물리적 일관성을 강제하므로 시각적 교란에 대한 견고성을 크게 향상할 수 있다. 또한 과거 trajectory에 noise(표준편차 0.02, STD)를 주입하면 Level 1에서 일반화 격차를 20%에서 52%로 더욱 줄일 수 있음을 확인했다.

### 초기 상태 불확실성

A2A에서는 후속 action sequence가 이전 sequence에 시간적으로 의존하므로, 과거 sequence의 불확실성에 대한 견고성이 어떠한지라는 자연스러운 의문이 제기된다. 이를 조사하기 위해 그림 [[XREF:initial_state]]과 같이 로봇의 초기 pose를 무작위화한다. 그림 [[XREF:FIGinitial]](왼쪽)의 결과는 각 step에서 순수 noise로부터 action을 생성하는 baseline과 비교할 때 A2A가 실제로 action history 내부의 불확실성에 더 민감함을 보여준다. 그러나 과거 action에 소량의 *Gaussian* noise(표준편차 0.1, STD)를 주입하면 일반화 성능이 크게 향상됨을 확인할 수 있다. 그림 [[XREF:FIGinitial]](오른쪽)은 성공률과 주입한 noise의 강도 사이의 관계를 추가로 보여준다. 결정성과 확률성 사이의 균형을 맞추기 위해 깨끗한 과거 데이터와 *Gaussian* noise를 최적으로 융합하는 방법은 향후 연구의 흥미로운 방향으로 남아 있다.

## Ablation study

아키텍처 설계에 관한 ablation study를 추가로 수행하여 두 가지 근본적인 질문에 답한다. 즉, 생성 패러다임이 결정론적 regression baseline보다 우수한 성능을 제공하는지, 그리고 latent space 내에서 flow matching을 수행하는 것이 원시 action space에서 직접 수행하는 것보다 더 효과적인지를 살펴본다.

### Regression 또는 생성

[[FIGURE:structure_ablation]]

**모델 구조의 ablation study.** 설정: *Close Box*, 30 epochs, 시연 수 100, flow 기반 방법은 6 inference steps. **왼쪽:** 학습 objective와 representation space의 영향. latent space와 원시 action space 각각에서 구현한 flow matching 전략과 regression 전략을 비교한다. **오른쪽:** 일반화 능력. 다양한 환경 교란하에서 latent-space regression과 flow matching의 견고성을 비교한다.

로봇 제어의 맥락에서 *생성*과 *regression*의 상대적 장점에 관한 논의가 증가하고 있다 [[CITE:pan2025much]]. 여기서는 flow matching objective를 결정론적 regression 접근법으로 대체하는 것도 시도한다. 공정한 비교를 위해 encoder와 latent space 설정을 포함한 다른 모든 아키텍처 구성요소는 엄격히 동일하게 유지한다. 결과는 그림 [[XREF:structure_ablation]](왼쪽)에 제시하며, 여기서 *Flow-latent*는 latent space 내에서 수행하는 flow matching, 즉 본 연구의 최종 선택을 나타낸다. *Reg-latent*는 latent space 내에서 수행하는 결정론적 regression을 나타낸다. 두 방법 모두 학습 분포에서 높은 성공률을 달성하며, 이는 최근 연구 결과와 일치함을 확인했다 [[CITE:pan2025much]]. 그러나 그림 [[XREF:structure_ablation]](오른쪽)은 생성 접근법이 환경 교란에 훨씬 더 높은 회복력을 보이는 반면, regression 변형은 이전에 보지 못한 시나리오로 일반화하지 못함을 보여준다.

이 격차는 action 입력과 시각 입력의 decoupling에서 비롯될 수 있다. regression 방법에서 더 고차원인 시각 representation과 직접 결합하면 저차원 proprioceptive signal의 이점이 희석될 수 있다.

### Action space 또는 latent space

latent space 없이 수행하는 flow matching을 U-Net backbone과 MLP backbone(A2A와 동일)을 모두 사용하여 추가로 평가한다. 결과는 그림 [[XREF:structure_ablation]](왼쪽)에 제시하며, 여기서 *Flow-action-UNet*은 U-Net 아키텍처를 사용해 원시 action space에서 직접 수행하는 flow matching을 나타내고, *Flow-action-MLP*는 MLP 아키텍처를 사용해 원시 action space에서 직접 수행하는 flow matching을 나타낸다. 원시 action space에서의 flow matching은 latent-space 접근법보다 열등한 수렴 성능으로 이어짐을 확인할 수 있다. 그 이유는 latent space의 고차원 representation이 flow의 초기 분포와 목표 분포를 효과적으로 정렬하기 때문이라고 볼 수 있다. 이러한 구조화된 정렬은 더 원활한 학습 과정을 촉진하여, 그림 [[XREF:latent_space]] 및 [[XREF:latent_space_appen]]과 같이 모델이 단일 step 추론 regime에서도 높은 성능을 달성할 수 있게 한다.

[[FIGURE:video_generation]]

**비디오 생성 결과.** 이전에 보지 못한 네 가지 서로 다른 시나리오에서 예측한 세 번째 frame을 시각화한다.
