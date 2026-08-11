# Action-to-Action Flow Matching

## 초록

Diffusion 기반 policy는 최근 action 예측을 조건부 denoising 과정으로 정식화함으로써 로보틱스에서 괄목할 만한 성공을 거두었다. 그러나 무작위 *Gaussian* noise에서 sampling하는 표준 관행은 깨끗한 action을 생성하는 데 여러 번의 반복 단계가 필요한 경우가 많으며, 이로 인해 높은 추론 지연이 발생하여 실시간 제어의 주요 병목이 된다. 본 논문에서는 정보가 없는 noise sampling의 필요성에 의문을 제기하고, 무작위 sampling에서 이전 proprioceptive action의 정보를 활용하는 초기화로 전환하는 새로운 policy 패러다임인 Action-to-Action flow matching(A2A)을 제안한다. proprioceptive action 피드백을 정적인 조건으로 취급하는 기존 방법과 달리, A2A는 과거 proprioceptive 시퀀스를 활용하여 이를 action 생성을 위한 시작점으로서 고차원 latent space에 embedding한다. 이 설계는 로봇의 물리적 동역학과 시간적 연속성을 효과적으로 포착하면서 비용이 많이 드는 반복적 denoising을 우회한다.

광범위한 실험은 A2A가 높은 학습 효율, 빠른 추론 속도, 향상된 일반화 성능을 보임을 입증한다. 특히 A2A는 단 한 번의 추론 단계만으로도 고품질 action 생성을 가능하게 하며, 시각적 교란에 대한 뛰어난 강건성과 보지 못한 구성에 대한 향상된 일반화 성능을 보인다. 마지막으로 A2A를 비디오 생성으로도 확장하여 시간적 모델링에서의 더 폭넓은 범용성을 입증한다. 프로젝트 사이트: https://lorenzo-0-0.github.io/A2A_Flow_Matching.

[[FIGURE:framework]]

**로봇 policy 패러다임 비교.** (a) Regression Policy: 다중 모달 입력에서 action으로의 결정론적 매핑. (b) Diffusion Policy: *Gaussian* noise로부터의 반복적 denoising을 통한 생성 모델링. (c) A2A Policy: 과거 action과 미래 action 사이의 구조화된 flow를 통한, 정보에 기반한 action 생성. *Action-to-action*은 *noise-to-action*보다 더 효율적인 transport를 가능하게 하며, 경량 MLP 아키텍처에서도 단일 단계 flow 매핑을 실현할 수 있게 한다.

# 서론

모방학습 아키텍처의 최근 발전은 복잡하고 비정형적인 환경에서 작동하는 로봇 시스템의 역량을 크게 확장했다[[CITE:ai2025review]]. 그중에서도 diffusion 기반 policy[[CITE:ddpm,flowmatching,dp,intelligence2025pi]]는 인간 시연에 내재한 다중 모달성을 모델링하는 강력한 패러다임으로 부상했다. 이 방법들은 action 생성을 조건부 denoising 과정으로 정식화한다. 학습 중에는 신경망이 주입된 noise를 예측하도록 학습하고, 추론 시에는 무작위 noise로 초기화된 sample을 반복적으로 denoising하여 실행 가능한 action을 얻는다.

고정밀 및 다중 모달 task에서 강력한 경험적 성능을 보임에도 불구하고, diffusion 모델에는 잘 알려진 한계가 있다. 즉, “처음부터 denoising”하는 패러다임은 상당한 추론 지연을 초래한다[[CITE:pan2025much]]. 하나의 action을 생성하는 데 일반적으로 수십 번의 반복적 denoising 단계가 필요하며, 낮은 cycle time과 빠른 피드백이 안정적인 실행에 필수적인 실시간 로봇 제어에서 이는 주요 병목을 만든다.

이 한계를 완화하기 위해 선행 연구는 추론을 가속하도록 diffusion 과정의 초기화를 개선하는 방안을 탐구했다. 예를 들어 [[CITE:steeringdp]]는 초기 sampling 분포를 유도하기 위해 RL로 학습한 policy를 제안하며, [[CITE:warmstarts]]는 더 유용한 시작점을 식별하기 위해 warm-start 전략을 사용한다. 이러한 접근법은 정보가 없는 *Gaussian* noise를 데이터 분포에 더 가까운 prior로 대체하며, 흔히 현재 관측을 조건으로 분포 통계량을 예측하는 보조 모델을 이용한다. 이러한 접근법은 효과적이지만 여전히 확률적 noise 초기화에 의존하며 필연적으로 추가적인 모델링 복잡성을 유발한다.

이러한 관찰은 더 근본적인 질문을 제기한다. **로봇 policy는 정말로 무작위 noise에서 sampling하여 생성해야 하는가?** Diffusion 모델은 본래 고충실도 이미지 합성과 비디오 생성을 위해 개발되었으며[[CITE:ddpm,song2020denoising,rombach2022high,flowmatching,rectifiedflow,blattmann2023stable]], 이 경우 의미 있는 prior가 없기 때문에 생성은 일반적으로 정보가 없는 noise에서 시작한다. 그러나 로봇 제어는 근본적으로 다른 체제에서 작동한다. 현대 로봇은 시스템의 구성과 동역학에 관한 연속적이고 지연이 짧은 피드백을 제공하는 풍부한 상태 센서를 갖추고 있다[[CITE:jia2024feedback,jia2024learning]]. 이 구조화된 피드백은 로봇의 현재 물리적 상태 또는 최근 실행 이력을 자연스럽게 encoding하는 강력하고 신뢰할 수 있는 prior를 이루며, 따라서 action 생성을 위한 무작위 noise 초기화의 원리적인 대안을 제공한다[[CITE:jia2025foreseer]].

그러나 [[XREF:framework]]의 (a)와 (b)에 나타낸 것처럼, 대부분의 기존 접근법은 현재 proprioceptive state/action과 시각 관측을 단순히 이어 붙인 것을 조건으로 action을 생성하는 regression 또는 diffusion 기반 패러다임 중 하나를 따른다. 이러한 설계는 로봇 motion에 내재한 시간적 연속성을 간과하며, 저차원 proprioceptive 신호를 고차원 시각 표현과 직접 융합할 때 이 신호를 약화하는 경우가 많다. 더욱이 최근 연구는 proprioceptive state에 대한 명시적 conditioning이 공간적 일반화에 악영향을 줄 수 있음을 보여준다[[CITE:zhao2025you]].

그 결과, 시스템 동역학과 action 추세에 관한 풍부한 과거 정보는 현재 널리 쓰이는 프레임워크에서 대체로 충분히 활용되지 못하고 있다. 주목할 점은 diffusion 모델이 개별 state 사이가 아니라 확률분포 사이의 매핑을 정의한다는 것이다. 이러한 관점은 자연스러운 질문으로 이어진다. 과거 실행 분포와 미래 action 분포 사이에 본질적으로 존재하는 근접성을 활용해 학습 복잡성을 줄이고, policy 생성을 위한 더 짧고 안정적인 transport 경로를 얻을 수 있는가?

이를 위해 본 논문은 action 생성을 *정보가 없는 sampling에서 정보에 기반한 초기화로* 전환하는 새로운 flow matching 기반 policy 패러다임인 **Action-to-Action Flow Matching(A2A)**을 제안한다. Diffusion 과정을 표준 *Gaussian* noise로 초기화하는 선행 접근법과 달리, A2A는 [[XREF:framework]]에 나타낸 것처럼 과거 proprioceptive action 시퀀스를 action 생성의 시작점으로 직접 활용한다. 미세한 motion 패턴과 시간적 의존성을 포착하기 위해 이러한 저차원 action 이력을 고차원 latent space에 embedding한다. 과거 action 분포를 미래 action으로 transport하는 flow를 학습함으로써 A2A는 *Gaussian* noise에서 출발하는 비용이 많이 드는 반복적 denoising 과정을 우회한다.

본 논문은 시뮬레이션 환경과 실제 로봇 시스템 모두에서 A2A를 광범위하게 평가한다. 경험적으로 본 방법은 탁월한 학습 효율을 보이며 최신 baseline 8개보다 일관되게 우수한 성능을 낸다.

특히 A2A는 vanilla diffusion 방법 및 flow matching 방법보다 각각 최대 $20\times$와 $5\times$ 빠르게 추론이 수렴하며, **단 한 번의 추론 단계만으로도 고품질 action 생성을 가능하게 한다**.

더욱이 생성 과정을 proprioceptive 이력에 기반하게 하면 시각적 교란에 대한 강건성이 크게 향상되며, 이력 정보를 활용한 초기화는 시간에 걸친 물리적 일관성을 강제함으로써 보지 못한 구성에 대한 일반화 성능을 높인다.

요약하면, 본 논문은 확률적 noise 초기화를 이력 기반 proprioceptive 초기화로 대체하여 로봇 자체의 동역학에 기반한, 정보에 입각한 action 생성을 가능하게 하는 새로운 diffusion 기반 로봇 policy 패러다임을 소개한다. A2A는 latent state 표현을 활용하여 세밀한 motion 구조를 포착하고 무작위 noise에서 반복적으로 denoising하지 않고도 효율적인 action-to-action 전환을 지원한다. 시뮬레이션 및 실제 로봇 환경에서 수행한 광범위한 실험은 본 방법이 학습 효율, 추론 속도, 시각적 교란에 대한 강건성, 보지 못한 구성에 대한 일반화 성능 모두에서 최신 성능을 달성함을 입증한다. 나아가 로봇 비디오 생성에 A2A를 적용할 수 있음을 보여주며, 이는 더 폭넓은 확장 가능성에 대한 유망한 잠재력을 시사한다.

# 관련 연구

## Visuomotor policy

Visuomotor policy는 원시 감각 관측, 일반적으로 고차원 시각 입력과 저차원 로봇 state를 저수준 제어 action으로 직접 매핑하는 로봇 학습 프레임워크이다. Action chunking(ACT)[[CITE:zhao2023learning]]과 같은 초기 접근법은 Transformer[[CITE:vaswani2017attention]]를 적용한 conditional variational autoencoder를 사용하여 미래 action 시퀀스를 예측함으로써 세밀한 양팔 조작을 학습했다. Diffusion policy[[CITE:dp]]는 action 분포를 score 기반 gradient field[[CITE:ddpm,song2020score]]로 모델링하여 diffusion 생성 패러다임을 도입했으며, 다중 모달 환경에서 안정성을 크게 향상했다. $\pi$ 계열[[CITE:intelligence2025pi,intelligence2025pi05,black2024pi_0]]과 같은 Vision-Language-Action(VLA) 모델에 사용되는 flow matching[[CITE:flowmatching]]은 noise 분포와 action 분포 사이의 직선 확률 경로를 학습하여 생성 과정을 단순화하고자 했다. 더 최근에는 [[CITE:pan2025much]]가 고급 모델 아키텍처(예: DiT[[CITE:Peebles_2023_ICCV]]와 UNet[[CITE:dp]]) 및 action chunking 전략[[CITE:zhao2023learning]]의 선택이 regression 방법보다 flow matching의 성공에 더 큰 영향을 미친다고 제시했다.

이러한 성공에도 불구하고 diffusion 방법은 반복적인 다단계 추론의 특성과 복잡한 아키텍처로 인해 계산 비용이 높다. 반대로 vision-to-action model(VITA)[[CITE:gao2025vita]]은 직접적인 vision-to-action 매핑에 경량 Multi-Layer Perceptron(MLP) backbone을 사용하여 아키텍처의 최소화를 추구한다. 그러나 VITA는 시각 입력에 전적으로 의존하므로 환경의 시각적 distractor에 취약하다. 또한 VITA의 flow space에는 차원 불일치가 존재한다. MeanFlow 기반 policy[[CITE:fang2025omp,geng2025mean]]와 consistency model[[CITE:zhang2025flowpolicy,li2026ofp,Consistency]] 같은 최근 연구는 noise-to-action 매핑의 이론적 경계를 최적화함으로써 단일 단계 생성을 로봇 action 예측에 도입하기 시작했다. 이와 달리 A2A는 action의 물리적 연속성을 활용하여 과거 proprioceptive action을 미래 action으로 직접 매핑함으로써 생성 경로를 근본적으로 단축하고 고성능 단일 단계 생성을 가능하게 한다.

## Diffusion의 noise 최적화

이미지 및 비디오 합성에서 초기 noise의 최적화는 생성 품질과 속도를 향상하는 핵심 전략이다[[CITE:ahn2024noise,mao2024lottery,samuel2024generating,eyring2024reno,warmstarts]]. 예를 들어 [[CITE:ahn2024noise]]는 경량 LoRA 모듈[[CITE:hu2022lora]]을 통해 표준 *Gaussian* noise를 guidance-free noise space로 매핑하도록 학습함으로써 계산 비용이 많이 드는 guidance 기법의 필요성을 없앤다. 마찬가지로 warm-start diffusion[[CITE:warmstarts]]은 deterministic 모델을 사용해 문맥을 바탕으로 초기 *Gaussian* 분포의, 정보에 기반한 평균과 분산을 제공하여 sampling 경로를 단축한다. 그러나 로보틱스에서 noise 최적화는 거의 연구되지 않았다. [[CITE:steeringdp]]는 latent-noise space에서 reinforcement learning을 수행하여 behavioral cloning policy를 조정함으로써 agent가 기반 policy의 weight를 변경하지 않고도 로봇 action을 유도할 수 있게 한다.

Noise-to-data 패러다임의 긴 transport 경로에서 벗어나 [[CITE:chen2024bridger]]는 유용한 초기 분포를 활용하지만, 여전히 heuristic 또는 사전학습 모델에 의존한다는 제약이 있다. 본 논문의 A2A는 action-to-action transport 메커니즘을 도입한다. 깨끗한 과거 데이터를 초기 분포로 직접 사용함으로써 로봇 motion의 물리적 연속성을 활용해 시작점을 고차원 latent space의 target에 훨씬 더 가깝게 배치한다. 이렇게 줄어든 분포 격차는 다단계 refinement의 필요성을 우회하여 실시간 로봇 제어에 최적화된 고충실도 단일 단계 추론을 가능하게 한다.
