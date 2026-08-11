# Action-to-action flow matching

## Flow matching

Robotics 분야에서 널리 채택되고 있다는 점을 고려하여[[CITE:black2024pi_0,intelligence2025pi,bjorck2025gr00t]], flow matching[[CITE:flowmatching]]을 algorithm의 기반으로 채택한다. Flow matching은 source distribution $p_0 = \mathcal{N}(\mathbf{0}, \mathbf{I})$를 $\mathbb{R}^d$상의 target data distribution $p_1 = p_{\text{data}}$로 변환하는 법을 학습하는 simulation-free training objective를 제공한다. $p_\tau: \mathbb{R}^d \to \mathbb{R}_{>0}$를 $\tau \in [0, 1]$에 대한 time-dependent probability density라 하며, 이는 $p_0$와 $p_1$ 사이를 보간하는 probability path를 정의한다. 이 path는 다음 ordinary differential equation(ODE)을 통해 time-dependent vector field $\mathbf{v}: [0, 1] \times \mathbb{R}^d \to \mathbb{R}^d$에 의해 생성된다.

[[EQUATION:1]]

$$
\frac{d\mathbf{x}_\tau}{d\tau} = \mathbf{v}_\tau(\mathbf{x}_\tau), \qquad \mathbf{x}_0 \sim p_0,
$$

여기서 $\mathbf{x}_\tau \in \mathbb{R}^d$는 flow time $\tau$에서의 state를 나타낸다.

[[FIGURE:pipeline]]

**A2A architecture 개요.** Framework는 세 가지 주요 component로 구성된다. 1) ResNet-18 backbone과 linear projector를 사용해 visual observation을 encode하여 global condition $c$를 생성하는 condition path. 2) Kernel size가 5인 CNN을 사용해 $n$-frame history action을 latent starting point $\mathbf{z}_0$로 compress하는 source path. 3) Flow 기반 generation process. AdaLN-MLP block으로 구성된 flow net은 통합된 512-dimensional latent space 내에서 $\mathbf{z}_0$를 target latent $\mathbf{z}_1$로 transport하기 위한 vector field를 예측한다. 마지막으로 residual MLP decoder가 $\mathbf{z}_1$을 future action sequence로 변환한다.

Optimal transport displacement map[[CITE:flowmatching]]을 채택하며, 이는 $\mathbf{x}_\tau = (1 - \tau)\mathbf{x}_0 + \tau \mathbf{x}_1$로 정식화된다. 목표는 $\mathbf{\theta}$로 parameterize된 neural network $f_\theta(\mathbf{x}_\tau, \tau, \mathbf{c})$를 학습하여 conditional vector field를 근사하는 것이며, 여기서 $\mathbf{c}$는 external conditioning(예: visual observation과 proprioceptive state)을 나타낸다. Flow matching loss는 다음과 같이 정의된다.

[[EQUATION:general_loss]]

$$
\mathcal{L}_{FM} = \mathbb{E}_{\tau \sim \mathcal{U}[0,1], \mathbf{x}_0\sim p_0, \mathbf{x}_1\sim p_1} \left\| f_\theta(\mathbf{x}_\tau, \tau, \mathbf{c}) - \mathbf{v}_\tau(\mathbf{x}_\tau) \right\|^2.
$$

학습된 $f_\theta(\mathbf{x}_\tau, \tau, \mathbf{c})$를 사용한 inference phase의 sampling은 일반적으로 discretized *Euler* integration을 통해 수행한다.

## Action to action flow

*Gaussian* distribution에서 denoise하는 기존 generation 기반 policy[[CITE:ddpm,flowmatching,dp]]와 달리, A2A는 Figure [[XREF:framework]](c)에 나타낸 것처럼 proprioceptive historical action space에서 future action space로 이어지는 policy를 학습하는 것을 목표로 한다. Action $\mathbf{a}$의 formulation은 task에 따라 달라지며 joint position과 end-effector state를 비롯한 다양한 control modality를 수용할 수 있다. Simulation에서는 joint angle을, experiment에서는 end-effector state를 선택하였다. Historical action $\mathbf{a}_{\leq t} = \{\mathbf{a}_{t-n+1}, \dots, \mathbf{a}_t\}$[^1], visual observation $\mathbf{I}_{\leq t}= \{\mathbf{I}_{t-m+1}, \dots, \mathbf{I}_t\}$, next action $\mathbf{a}_{> t} = \{\mathbf{a}_{t+1}, \dots, \mathbf{a}_{t+n}\}$가 주어지며, 여기서 $n$과 $m$은 각각 action horizon과 observation horizon을 나타낸다. A2A framework는 공유 latent space $\mathcal{Z}$에서의 conditional flow를 통해 historical action의 distribution을 future action의 distribution으로 직접 변환한다.

[^1]: Closed-loop robustness를 높이기 위해, $\mathbf{a}_{\leq t}$는 이전에 command한 action이 아니라 proprioceptive feedback으로부터 추론한 *실제로 실행된* action의 history를 나타내며, 이는 불완전한 low-level tracking을 고려한 것이다.

Figure [[XREF:pipeline]]은 A2A architecture를 상세히 보여 준다. 구체적으로, 제안 architecture는 Convolutional Neural Network(CNN) 기반 autoencoder를 활용하여 action trajectory를 compact latent space $\mathcal{Z}$로 mapping한다. 구체적으로 action encoder $E_a$와 decoder $D_a$는 mapping $\mathbf{z}_0 = E_a(\mathbf{a}_{\leq t})$와 reconstruction $\hat{\mathbf{a}}_{>t} = D_a(\mathbf{z}_1)$을 parameterize한다. 동시에 visual encoder $E_I$는 multi-modal image stream $\mathbf{I}_{\leq t}$에서 feature를 추출하고, 이 feature를 MLP를 통해 추가로 project하여 global conditioning vector $\mathbf{c} = \mathrm{MLP}(E_I(\mathbf{I}_{\leq t}))$를 형성한다. 마지막으로 $\tau \in [0, 1]$에 대해 ODE ${d\mathbf{z}_\tau}/{d\tau} = \mathbf{v}_\tau(\mathbf{z}_\tau)$를 만족하는 time-dependent vector field $\mathbf{v}_\tau$를 통해 $\mathcal{Z}$에서 action-to-action flow를 정의한다.

연속적인 robot motion의 물리적 일관성으로 인해 인접한 action chunk에는 본질적인 유사성이 존재한다. 이러한 segment를 high-dimensional latent space에 추가로 embedding하고 flow matching으로 학습하면, starting point $\mathbf{z}_0$의 distribution이 target $\mathbf{z}_1$과 잘 정렬된다(Figure [[XREF:latent_space]] 및 Figure [[XREF:latent_space_appen]] 참조). 이처럼 distributional distance가 감소하면 transport mapping이 크게 단순해져, 경량 MLP도 single-step inference만으로 강력한 성능을 달성할 수 있다.

Historical action $\mathbf{a}_{\leq t}$에 미세한 noise를 가하여 stochasticity를 도입하고 어느 정도의 multimodality를 보존할 수도 있음에 유의한다(Figure [[XREF:multi_modal]]). Action-level uncertainty가 존재할 때 A2A는 앞선 action sequence에 본질적으로 의존하기 때문에 성능이 저하된다. Encoding stage 전에 historical action에 미세한 stochastic perturbation을 주입하면 이러한 uncertainty에 대한 generalization capability를 크게 높일 수 있다. Section [[XREF:sec-initial_state]]에서는 이 mechanism의 효과를 뒷받침하는 empirical evidence를 제시한다.

## Learning objectives

전체 training objective $\mathcal{L}_{total}$은 generation accuracy와 physical consistency를 동시에 보장하기 위한 multi-task loss로 정식화한다.

**Flow matching loss.** 주요 objective는 latent space $\mathcal{Z}$에서 time-dependent vector field $f_\theta(\mathbf{z}_\tau, \tau, \mathbf{c})$를 regression하는 것이다. 이 loss는 model이 latent starting action $\mathbf{z}_0$와 latent target action $\mathbf{z}_1$ 사이의 optimal transport path를 학습하도록 보장하며, 즉 다음과 같다.

[[EQUATION:action_flow_loss]]

$$
\mathcal{L}_{FM} = \mathbb{E}_{\tau \sim \mathcal{U}[0,1], \mathbf{z}_0, \mathbf{z}_1} \left\| f_\theta(\mathbf{z}_\tau, \tau, \mathbf{c}) - \mathbf{v}_\tau(\mathbf{z}_\tau, \tau, \mathbf{c}) \right\|^2.
$$

Equation [[XREF:action_flow_loss]]은 action latent space $\mathcal{Z}$에서 Equation [[XREF:general_loss]]을 구체화한 A2A formulation이다.

**Autoencoder reconstruction loss.** Latent space $\mathcal{Z}$가 action space의 topological structure를 보존하도록 action autoencoder에 $\ell_1$ reconstruction loss를 적용하며, 즉 다음과 같다.

[[EQUATION:4]]

$$
\mathcal{L}_{AE} = \mathbb{E}_{\mathbf{a}_{> t}} \left\| \mathbf{a}_{> t} - D_a(E_a(\mathbf{a}_{> t})) \right\|_1.
$$

이 loss는 encoder $E_a$와 decoder $D_a$를 regularize하여 action chunk의 high-fidelity reconstruction을 유지하게 한다.

**Inference consistency loss.** Abstract latent generation과 physical execution 사이의 간극을 해소하기 위해, 기존 연구[[CITE:gao2025vita]]에서 영감을 받아 inference consistency loss를 도입한다. Inference consistency는 latent space와 original action space 모두에서 ODE로 inference한 action과 ground-truth action을 정렬하는 것을 목표로 하며, 즉 다음과 같다.

[[EQUATION:loss_IC]]

$$
\mathcal{L}_{IC} = \mathbb{E}_{\hat{\mathbf{z}}_1, \mathbf{a}_{> t}} \left\| \hat{\mathbf{z}}_1 - E_a(\mathbf{a}_{> t}) \right\|_1 + \lambda_0\mathbb{E}_{\hat{\mathbf{z}}_1, \mathbf{a}_{> t}} \left\| D_a(\hat{\mathbf{z}}_1) - \mathbf{a}_{> t} \right\|_1,
$$

여기서 $\hat{\mathbf{z}}_1$은 ODE integration으로 얻은 latent vector이고, $\lambda_0\in \mathbb{R}_{>0}$는 사용자가 정의한 weight를 나타낸다. 이 objective는 생성된 flow trajectory가 물리적으로 의미 있고 실행 가능한 action으로 변환되도록 보장한다. 기존 연구[[CITE:gao2025vita]]에서는 $\mathcal{L}_{IC}$가 latent space collapse를 방지하는 데 핵심적임을 확인하였다.

마지막으로 전체 training objective $\mathcal{L}_{total}$은 세 weighting coefficient $\lambda_1$, $\lambda_2$, $\lambda_3 \in \mathbb{R}_{>0}$를 사용하여 다음과 같이 정식화한다.

[[EQUATION:6]]

$$
\mathcal{L}_{total} = \lambda_1\mathcal{L}_{FM} + \lambda_2\mathcal{L}_{AE} + \lambda_3\mathcal{L}_{IC}.
$$
