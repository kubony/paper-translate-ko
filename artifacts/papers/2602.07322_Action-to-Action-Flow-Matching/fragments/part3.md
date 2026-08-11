[[FIGURE:video_generation]]

**Video generation 결과.** 서로 다른 네 가지 미관측 시나리오에서 예측한 세 번째 frame을 시각화한다.

# Video generation에의 적용

Robotic manipulation과 마찬가지로, 미래 frame 예측 형태의 video generation은 본질적으로 시간적 연속성 과제이다. 고충실도 미래 video 예측은 VLA model의 성능을 향상시킬 수 있다[[CITE:zhao2025cot,deng2026video]]. 본 연구에서는 A2A paradigm의 video generation에 대한 전이 가능성을 더 탐구하며, 이를 이하 **F**rames-to-**F**rames flow matching(**F2F**)이라 한다. Training dataset은 *pick cube* task의 각 level(Level 0–4)당 100개의 video로 구성되며, test set은 동일한 task의 미관측 시나리오 네 가지로 구성된다. F2F는 연속된 세 frame의 history를 바탕으로 미래 frame 세 개를 예측하도록 설계된다. F2F와 baseline은 모두 500 epoch 동안 학습한다. 구현 세부 사항은 Appendix [[XREF:appen_video]]를 참조한다. Figure [[XREF:video_generation]]에 나타낸 바와 같이, F2F는 동일한 network 구성으로 구현한 regression 기반 baseline보다 현저히 높은 생성 품질을 달성한다. 이 결과는 소규모 model로 달성한 것이지만, F2F paradigm은 더 큰 architecture로 확장할 잠재력이 크다. 향후 연구에서는 A2A의 성능을 더욱 높이기 위해 예측 video를 policy architecture에 통합하는 방안을 더 추구할 것이다.

# 결론

본 논문에서는 noise 기반 initialization을 action-to-action transport로 대체하는 효율적인 generative paradigm인 A2A를 제안한다. A2A는 연속 motion의 물리적 일관성을 활용하여 시작 distribution과 target distribution을 정렬하며, 이를 통해 경량 MLP가 최소 latency로 높은 success rate를 달성할 수 있게 한다. 다양한 simulation 및 real-world robotic benchmark 전반에서 A2A는 state-of-the-art diffusion 및 flow 기반 policy와 대등하거나 이를 능가하는 동시에 inference를 더 적은 step으로 줄인다. 이 접근법은 diffusion 기반 policy에서 일반적으로 나타나는 계산 병목을 효과적으로 제거한다. Robotics와 video generation을 넘어, 이 framework는 본질적으로 다양한 연속 시간 과제에 적합하며, 순차적 연속성을 특징으로 하는 domain에서의 잠재력은 향후 탐구할 유망한 방향으로 남아 있다.

# 한계

A2A는 action의 물리적 연속성에 기반하므로, 부드럽고 연속적인 control signal이 지배적인 task에서 가장 효과적이다. Binary gripper open/close command와 같은 discrete 또는 switch형 action dimension에서는 이러한 연속성 prior가 제공하는 이점이 제한적이다. 또한 현재 objective는 여러 loss-weighting coefficient를 수동으로 tuning해야 한다. Adaptive loss weighting과 hybrid continuous-discrete action space 지원은 향후 연구의 유망한 방향으로 남겨 둔다.

# 부록

## Randomization level 설정

평가 대상 method의 robustness를 체계적으로 평가하기 위해, simulation environment에 stochastic perturbation을 도입하는 *Roboverse*의 계층적 generalization level을 활용한다. 이 절에서는 Level 0(object randomization), Level 1(+background randomization), Level 2(+lighting randomization), Level 3(+camera viewpoint randomization)의 구성을 상세히 설명한다.

Level 0은 Figure [[XREF:level0]]에 나타낸 것처럼 초기 object position의 randomization을 도입한다. 이는 평가 대상 algorithm의 training set 역할을 한다.

Level 1은 Figure [[XREF:level1]]에 나타낸 것처럼 주로 environment background의 randomization에 초점을 맞춘다. 이 level은 task와 무관한 visual distractor에 대한 policy의 robustness를 평가하도록 설계된다.

Level 2는 lighting randomization을 더 추가한다. Primary DiskLight(12k-45k intensity), auxiliary SphereLight(5k-20k intensity), ambient preset을 사용해 illumination을 randomize한다. Parameter에는 2500K부터 6500K까지의 color temperature, ceiling light에 대한 $\pm 15^\circ$의 directional jitter, 다양한 shadow pattern을 생성하기 위한 sphere light의 $\pm 0.5$m(lateral/longitudinal) 및 $\pm 0.3$ m(vertical) positional offset이 포함된다.

Level 3은 camera viewpoint randomization을 추가로 구현한다. Camera extrinsic은 lateral/longitudinal shift에 대해 $\pm 20$cm의 delta 범위 내 uniform distribution을 사용하여 perturb한다. Vertical shift는 위쪽 방향의 $0$부터 $10$ cm 범위로 제한한다.

## Hyperparameter

모든 simulation과 experiment에 사용하는 training hyperparameter는 Table [[XREF:tab-parameters]]에 나타낸 것처럼 동일하게 설정한다. *Roboverse* platform의 표준 ACT 구현은 약 60M개의 parameter로 구성되며, 이는 DDPM-UNet($\approx$ 28M)의 거의 두 배임에 유의한다. 공정한 비교를 위해 ACT의 Transformer backbone을 수정하여 parameter 수를 절반으로 줄였고, 그 결과 평가한 모든 baseline에서 model scale을 정렬하였다.

[[TABLE:tab-parameters]]

**Training hyperparameter.**

| **Hyperparameter** | **값** |
|---|---:|
| n | 8 |
| m | 8 |
| $\lambda_0$ | 0.5 |
| $\lambda_1$ | 1 |
| $\lambda_2$ | 0.5 |
| $\lambda_3$ | 1 |
| Batch size | 32 |

## Experimental setup

Real test에서는 A2A를 Franka robotic platform에 deploy하며, training parameter를 simulation baseline과 완전히 동일하게 유지한다. Simulation environment와의 핵심적인 차이는 dual-view visual input을 사용한다는 것이며, 그 setup은 Figure [[XREF:camera_view]]에 나타낸다.

[[FIGURE:camera_view]]

**Real test에서의 camera view.**

## Video generation

Figure [[XREF:pipeline_f2f]]는 F2F algorithm의 architectural framework를 보여 주며, historical frame sequence에서 future prediction으로의 전환을 나타낸다. Historical frame $I_{\leq t}$를 ResNet18 backbone과 VAE head를 사용해 512-dimensional latent space로 encode하여 initial state $z_0$를 얻는다. 4개 layer와 4개 attention head로 구성된 Flow Net Transformer는 $z_0$를 target latent $z_1$에 mapping하는 vector field $v$를 학습한다. 이어서 5-layer convolutional upsampling decoder를 통해 future frame $I_{> t}$를 reconstruct한다. Baseline으로는 historical sequence로부터 future frame을 직접 예측하는 deterministic regression model을 사용한다. 공정한 비교를 위해 flow matching training objective를 생략한 것을 제외하면 baseline은 F2F와 동일한 architecture를 유지한다.

평가 중에는 서로 보완적인 네 가지 metric인 Peak Signal-to-Noise Ratio(PSNR), Structural Similarity Index Measure(SSIM), Mean Squared Error(MSE), Learned Perceptual Image Patch Similarity(LPIPS)를 사용하여 예측 성능을 평가한다.

[[FIGURE:pipeline_f2f]]

**Video prediction을 위한 F2F architecture 개요.** Model은 ResNet-VAE architecture를 활용하여 historical observation을 latent space로 compress하고, 이 공간에서 Transformer 기반 flow matching이 future state로의 transport를 계산한다. 예측 sequence $I_{> t}$는 convolutional upsampling block을 통해 생성된다.

[[FIGURE:iterations_ddpm_fm]]

**DDPM-UNet과 FM-UNet의 training efficiency에 대한 추가 test.**

[[FIGURE:level0]]

**Randomization Level 0.** Level 0은 초기 object position의 randomization을 도입한다. 이는 training set 역할을 한다.

[[FIGURE:level1]]

**Randomization Level 1.** Level 1은 주로 environment background의 randomization에 초점을 맞춘다.

[[FIGURE:latent_space_appen]]

***Pick Cube*와 *Stack Cube* task에서 latent space representation의 convergence.** History action latent와 future action latent를 함께 embedding하기 위해 t-SNE를 적용하고, paired sample을 선으로 연결한다. 선의 색은 512-dimensional latent space에서 계산한 distance를 나타낸다.

[[FIGURE:initial_state]]

**Initial state uncertainty.** Action-level uncertainty에서의 generalization 성능을 조사하기 위해 robot의 initial pose를 randomize한다.

[[FIGURE:multi_modal]]

**미세한 action noise가 multimodal behavior를 가능하게 한다.** Agent가 장애물 사이의 틈을 통과하여 시작점(빨간색 $\star$)에서 target(빨간색 $\oplus$)에 도달해야 하는 2D navigation task이며, 위쪽 장애물의 왼쪽 또는 오른쪽으로 이동하는 본질적으로 multimodal한 optimal solution이 존재하는 setting이다. (a) A2A policy는 사실상 deterministic하다. Multimodal training data에도 불구하고 rollout이 단일 mode로 collapse한다. (b) Historical action $\mathbf{a}_{\leq t}$에 std $\sigma=0.02$인 zero-mean *Gaussian* noise를 추가하면 task success를 희생하지 않고 이러한 determinism이 깨져, policy가 여러 rollout에 걸쳐 두 mode를 모두 표현할 수 있다. 이는 학습된 policy의 multimodality를 보존하기 위한 경량 mechanism으로 action perturbation을 채택한 본 연구의 design choice를 입증한다.
