# 평가

[[TABLE:tab-30epochs]]

9가지 서로 다른 알고리즘에서 5개 simulation 과제에 대한 성공률(100개 시연, 30 에포크). 최고 결과는 **굵게** 표시하고, 두 번째로 좋은 결과는 <u>밑줄</u>로 표시한다.

| **방법** | **스텝** | **Close Box** (%) | **Pick Cube** (%) | **Stack Cube** (%) | **Open Drawer** (%) | **Pick-Place Bowl** (%) |
|---|---:|---:|---:|---:|---:|---:|
| **A2A-Flow** | 6 | **92** | **92** | **86** | **92** | <u>90</u> |
| VITA | 6 | <u>88</u> | <u>88</u> | <u>80</u> | <u>90</u> | **92** |
| FM-UNet | 10 | 82 | 70 | 28 | 34 | 68 |
| FM-DiT | 10 | 58 | <u>88</u> | 26 | 28 | 84 |
| DDPM-UNet | 100 | 72 | 60 | 36 | 64 | 66 |
| DDPM-DiT | 100 | 58 | 58 | 16 | 14 | 68 |
| DDIM-UNet | 40 | 70 | 56 | 36 | 64 | 82 |
| Score-UNet | 100 | 36 | 36 | 12 | 0 | 4 |
| ACT | 1 | 82 | 86 | 32 | 80 | 60 |

제안하는 A2A-Flow를 *Roboverse* 플랫폼[[CITE:geng2025roboverse]]의 5개 simulation 과제(ManiSkill[[CITE:mu2021maniskill]]의 *Stack Cube* 및 *Pick Cube*, RLBench[[CITE:james2020rlbench]]의 *Close Box*, LIBERO[[CITE:liu2023libero]]의 *Open Drawer* 및 *Pick-Place Bowl*)와 *Franka* 로봇의 2개 실제 환경 과제(*Pick Cube* 및 *Open Drawer*)에서 포괄적으로 평가하며, 이는 [[XREF:experiments]], [[XREF:real_test]], [[XREF:real_test_close]]에 제시한다. 성능은 DDPM-UNet[[CITE:dp,ddpm]], DDPM-DiT[[CITE:ddpm,Peebles_2023_ICCV]], DDIM-UNet[[CITE:dp,song2020denoising]], FM-UNet[[CITE:flowmatching]], FM-DiT[[CITE:flowmatching,Peebles_2023_ICCV]], Score-UNet[[CITE:song2020score]], ACT[[CITE:zhao2023learning]], VITA[[CITE:gao2025vita]]를 포함한 8개의 최첨단 기준 방법과 비교한다. 공정하고 엄밀한 비교를 보장하기 위해 평가하는 모든 방법에서 하이퍼파라미터(예: 청크 크기, 배치 크기)와 네트워크 규모를 가능한 한 최대한 동일하게 설정했다. 평가는 주로 훈련 효율성, 추론 비용, 일반화에 초점을 맞춘다. 모든 실험에서 $\lambda_0 = 0.5$, $\lambda_1 = 1$, $\lambda_2 = 0.5$, $\lambda_3 = 1$, $n = m = 8$ 및 배치 크기 32를 사용한다(부록 [[XREF:appen_param]]).

[[FIGURE:experiments]]

**Simulation 과제.** Simulation은 *Roboverse* 플랫폼[[CITE:geng2025roboverse]]에서 수행한다. 구현한 과제에는 ManiSkill[[CITE:mu2021maniskill]]의 *Stack Cube* 및 *Pick Cube*, RLBench[[CITE:james2020rlbench]]의 *Close Box*, LIBERO[[CITE:liu2023libero]]의 *Open Drawer* 및 *Pick-Place Bowl*이 포함된다.

## 훈련 효율성

[[FIGURE:training_efficiency]]

**훈련 효율성 시험.** **왼쪽:** 훈련 에포크 수를 달리했을 때의 성공률(*Close Box* 과제에서 100개 시연 사용). **오른쪽:** 시연 수를 달리했을 때의 성공률(*Stack Cube* 과제에서 100 에포크).

먼저 서로 다른 훈련 데이터 크기와 에포크 수에서 A2A-Flow의 성능을 분석한다. [[XREF:training_efficiency]]는 평가한 모든 방법의 훈련 효율성을 보여준다. [[XREF:training_efficiency]](왼쪽)에 제시된 것처럼 A2A-Flow는 DDPM-UNet 및 FM-UNet보다 우수한 수렴 속도를 보이며, *Close Box* 과제에서 크게 제한된 40 훈련 에포크 이내에 안정적인 100% 성공률을 달성한다.

또한 [[XREF:training_efficiency]](오른쪽)의 샘플링 효율성 결과는 시연 수가 증가함에 따라 A2A-Flow가 높은 성능 상한에 빠르게 도달하고 이를 유지함을 보여준다. 이와 대조적으로 DDPM-UNet과 FM-UNet은 모두 눈에 띄는 변동과 더 낮은 안정성을 보인다. 이러한 차이는 *Stack Cube* 과제의 데이터셋이 증가하면서 trajectory 다양성이 커지는 데서 비롯된 것으로 보이며, 이를 수용하려면 더 큰 모델 용량 또는 더 많은 훈련 에포크가 필요할 수 있다. 이 가설을 검증하기 위해 DDPM-UNet 및 FM-UNet 기준 방법을 추가로 평가한다. [[XREF:iterations_ddpm_fm]]에 제시된 것처럼 이들의 성공률은 훈련 에포크가 증가함에 따라 점차 100%로 수렴한다.

[[FIGURE:real_test]]

***Pick Cube* 과제의 실험 결과.** (a) 제한된 30개 trajectory 데이터셋으로 policy를 100 에포크 동안 훈련한다. 평가 시 각 방법을 10회 시행에 걸쳐 시험한다. (b) 목표물을 이전에 보지 못한 발광 블록으로 교체하여 일반화 능력을 한층 더 시험한다. (c) 제한된 10개의 훈련 시연으로 서로 다른 위치에서 큐브를 집는다.

[[FIGURE:real_test_close]]

***Open Drawer* 과제의 실험 결과.** 제한된 30개 trajectory 데이터셋으로 policy를 300 에포크 동안 훈련한다. 시간 비용은 과제 완료 과정에서 경과한 총시간을 뜻한다. 성공률은 10회 시행에 걸쳐 평가한다.

[[XREF:real_test]](a)와 [[XREF:real_test_close]](a)의 실제 환경 시험은 훈련 trajectory가 30개뿐인 경우에도 A2A-Flow가 100%의 분포 내 성공률을 달성하여 DDPM-UNet과 FM-UNet을 능가함을 추가로 보여준다. [[XREF:real_test_close]](b)는 제안하는 알고리즘이 *Open Drawer* 과제에서 더 짧은 완료 시간을 달성하는 반면, DDPM-UNet과 FM-UNet은 동작 중에 상당한 주저를 보인다는 점을 추가로 보여준다. 또한 집기 위치 시험을 추가로 수행한다. 2개의 집기 위치를 더 추가하며([[XREF:real_test]](c)), 각 위치에는 시연이 10개뿐이다. A2A-Flow는 빠른 적응과 높은 성공률을 보여주며 새로운 시나리오에서 우수한 데이터 효율성을 입증한다. 시야각(FOV)의 가장자리(오른쪽 아래 위치, [[XREF:camera_view]])에서도 A2A-Flow는 유효한 성공률을 유지하며, 최적이 아닌 시각 입력에 대한 견고성을 분명히 보여준다.

이러한 결과는 A2A-Flow policy가 특히 훈련 데이터가 제한되고 훈련 에포크 수가 적은 조건에서 우수한 성능을 달성함을 나타낸다.

5개의 서로 다른 과제와 9개 알고리즘에 대한 정량적 결과는 [[XREF:tab-30epochs]]에 요약한다. A2A-Flow는 일관되게 가장 높은 성공률을 달성한다. 마찬가지로 추론 일관성 메커니즘[[CITE:gao2025vita]]을 도입한 VITA도 경쟁력 있게 높은 성공률을 달성한다. 특히 고급 transformer 아키텍처와 동일한 하이퍼파라미터가 주어졌을 때 회귀 기반 ACT가 생성 기반 방법에 필적하는 성능을 달성한다는 사실을 확인했다. 이러한 관찰은 [[CITE:pan2025much]]의 최근 발견과 일치한다.
