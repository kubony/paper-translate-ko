<!-- source lines: 10–196 -->

## 초록

본 논문에서는 강화학습을 위한 새로운 policy gradient 방법군을 제안한다. 이 방법들은 환경과의 상호작용을 통해 데이터를 표본추출하는 단계와 stochastic gradient ascent를 사용하여 “surrogate” objective function을 최적화하는 단계를 번갈아 수행한다. 표준 policy gradient 방법은 데이터 표본당 한 번의 gradient update를 수행하지만, 본 논문에서는 여러 epoch의 minibatch update를 가능하게 하는 새로운 objective function을 제안한다. proximal policy optimization(PPO)이라 명명한 이 새로운 방법은 trust region policy optimization(TRPO)의 장점 일부를 지니면서도 구현이 훨씬 간단하고, 더 일반적이며, 경험적으로 더 나은 sample complexity를 보인다. 실험에서는 시뮬레이션된 로봇 locomotion과 Atari 게임 플레이를 비롯한 여러 benchmark task에서 PPO를 검증하며, PPO가 다른 online policy gradient 방법보다 우수하고 sample complexity, 단순성, wall-time 사이에서 전반적으로 유리한 균형을 이룸을 보인다.

## 1 서론

최근 몇 년간 neural network function approximator를 사용하는 강화학습을 위해 여러 접근법이 제안되었다. 주요 후보로는 deep Q-learning [Mni+15], “vanilla” policy gradient 방법 [Mni+16], 그리고 trust region / natural policy gradient 방법 [Sch+15b]이 있다. 그러나 확장 가능하고(대규모 model 및 병렬 구현으로 확장 가능하며), data-efficient하고, robust한(즉, hyperparameter tuning 없이 다양한 문제에서 성공하는) 방법을 개발하는 데에는 개선의 여지가 있다. Q-learning(function approximation을 사용하는 경우)은 많은 단순한 문제에서 실패하며[^1] 충분히 이해되어 있지 않고, vanilla policy gradient 방법은 data efficiency와 robustness가 낮다. 또한 trust region policy optimization(TRPO)은 비교적 복잡하며, noise를 포함하는 architecture(예: dropout)나 parameter sharing(policy와 value function 사이의 공유 또는 auxiliary task와의 공유)을 포함하는 architecture와 호환되지 않는다.

본 논문은 first-order optimization만을 사용하면서도 TRPO의 data efficiency와 신뢰할 수 있는 성능을 달성하는 algorithm을 도입함으로써 현재의 상황을 개선하고자 한다. 본 논문에서는 clipped probability ratio를 사용하는 새로운 objective를 제안하며, 이는 policy 성능의 비관적 추정치(즉, lower bound)를 형성한다. Policy를 최적화하기 위해 policy로부터 데이터를 표본추출하는 단계와 표본추출된 데이터에 대해 여러 epoch의 최적화를 수행하는 단계를 번갈아 진행한다.

실험에서는 surrogate objective의 여러 상이한 version의 성능을 비교하며, clipped probability ratio를 사용하는 version이 가장 우수한 성능을 보임을 확인한다. 또한 PPO를 문헌에 제시된 여러 기존 algorithm과 비교한다. Continuous control task에서 PPO는 비교 대상 algorithm보다 더 나은 성능을 보인다. Atari에서는 A2C보다 sample complexity 측면에서 상당히 우수하고 ACER와 유사한 성능을 보이면서도 훨씬 더 단순하다.

[^1]: DQN은 discrete action space를 사용하는 Arcade Learning Environment [Bel+15]와 같은 game environment에서는 잘 작동하지만, OpenAI Gym [Bro+16]에 포함되고 Duan et al. [Dua+16]이 기술한 것과 같은 continuous control benchmark에서 우수한 성능을 보인 바는 없다.

## 2 배경: Policy Optimization

### 2.1 Policy Gradient 방법

Policy gradient 방법은 policy gradient의 estimator를 계산한 뒤 이를 stochastic gradient ascent algorithm에 대입하는 방식으로 작동한다. 가장 널리 사용되는 gradient estimator는 다음과 같은 형태이다.

$$
\hat{g} = \hat{\mathbb{E}}_t\left[\nabla_\theta \log \pi_\theta(a_t \mid s_t)\hat{A}_t\right] \tag{1}
$$

여기서 $\pi_\theta$는 stochastic policy이고 $\hat{A}_t$는 timestep $t$에서 advantage function의 estimator이다. 여기서 기댓값 $\hat{\mathbb{E}}_t[\cdots]$는 표본추출과 최적화를 번갈아 수행하는 algorithm에서 유한한 sample batch에 대한 empirical average를 나타낸다. Automatic differentiation software를 사용하는 구현은 그 gradient가 policy gradient estimator가 되는 objective function을 구성하는 방식으로 작동하며, estimator $\hat{g}$는 다음 objective를 미분하여 얻는다.

$$
L^{PG}(\theta) = \hat{\mathbb{E}}_t\left[\log \pi_\theta(a_t \mid s_t)\hat{A}_t\right]. \tag{2}
$$

동일한 trajectory를 사용하여 이 loss $L^{PG}$를 여러 step에 걸쳐 최적화하는 것은 매력적으로 보이지만, 그렇게 할 타당한 근거가 충분하지 않으며 경험적으로도 흔히 policy update가 파괴적일 정도로 커진다(6.1절을 참조한다. 결과는 제시하지 않았지만 “clipping 또는 penalty 없음” 설정과 유사하거나 그보다 나빴다).

### 2.2 Trust Region 방법

TRPO [Sch+15b]에서는 policy update의 크기에 관한 constraint 아래에서 objective function(“surrogate” objective)을 최대화한다. 구체적으로 다음과 같다.

$$
\underset{\theta}{\operatorname{maximize}}\quad
\hat{\mathbb{E}}_t\left[
\frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\mathrm{old}}}(a_t \mid s_t)}\hat{A}_t
\right] \tag{3}
$$

$$
\text{subject to}\quad
\hat{\mathbb{E}}_t\left[\mathrm{KL}\left[\pi_{\theta_{\mathrm{old}}}(\cdot \mid s_t),\pi_\theta(\cdot \mid s_t)\right]\right] \leq \delta. \tag{4}
$$

여기서 $\theta_{\mathrm{old}}$는 update 이전의 policy parameter vector이다. Objective를 선형 근사하고 constraint를 이차 근사한 다음 conjugate gradient algorithm을 사용하면 이 문제를 효율적으로 근사하여 풀 수 있다.

실제로 TRPO를 정당화하는 이론은 constraint 대신 penalty를 사용할 것을 시사한다. 즉, 다음 unconstrained optimization problem을 푼다.

$$
\underset{\theta}{\operatorname{maximize}}\quad
\hat{\mathbb{E}}_t\left[
\frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\mathrm{old}}}(a_t \mid s_t)}\hat{A}_t
- \beta\,\mathrm{KL}\left[\pi_{\theta_{\mathrm{old}}}(\cdot \mid s_t),\pi_\theta(\cdot \mid s_t)\right]
\right] \tag{5}
$$

여기서 $\beta$는 어떤 coefficient이다. 이는 특정 surrogate objective(state에 걸친 평균 KL 대신 최대 KL을 계산한다)가 policy $\pi$의 성능에 대한 lower bound(즉, 비관적 bound)를 형성한다는 사실에서 도출된다. 여러 상이한 문제 전반에서, 심지어 학습 과정에 따라 특성이 변하는 하나의 문제 내에서조차 우수하게 작동하는 단일 $\beta$ 값을 선택하기 어렵기 때문에 TRPO는 penalty 대신 hard constraint를 사용한다. 따라서 TRPO의 monotonic improvement를 모방하는 first-order algorithm이라는 목표를 달성하려면, 고정된 penalty coefficient $\beta$를 단순히 선택하여 SGD로 penalty가 부과된 objective인 식 (5)를 최적화하는 것만으로는 충분하지 않으며 추가적인 수정이 필요함을 실험이 보여준다.

## 3 Clipped Surrogate Objective

Probability ratio $r_t(\theta)$를 $r_t(\theta)=\frac{\pi_\theta(a_t\mid s_t)}{\pi_{\theta_{\mathrm{old}}}(a_t\mid s_t)}$로 나타내면 $r_t(\theta_{\mathrm{old}})=1$이다. TRPO는 다음 “surrogate” objective를 최대화한다.

$$
L^{CPI}(\theta)
= \hat{\mathbb{E}}_t\left[
\frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\mathrm{old}}}(a_t \mid s_t)}\hat{A}_t
\right]
= \hat{\mathbb{E}}_t\left[r_t(\theta)\hat{A}_t\right]. \tag{6}
$$

위 첨자 $CPI$는 conservative policy iteration [KL02]을 가리키며, 이 objective는 해당 연구에서 제안되었다. Constraint가 없으면 $L^{CPI}$의 최대화는 지나치게 큰 policy update로 이어진다. 따라서 이제 $r_t(\theta)$가 1에서 멀어지도록 만드는 policy의 변화에 penalty를 부과하기 위해 objective를 어떻게 수정할지 살펴본다.

본 논문에서 제안하는 주된 objective는 다음과 같다.

$$
L^{CLIP}(\theta)
= \hat{\mathbb{E}}_t\left[
\min\left(
r_t(\theta)\hat{A}_t,
\operatorname{clip}\left(r_t(\theta),1-\epsilon,1+\epsilon\right)\hat{A}_t
\right)
\right]. \tag{7}
$$

여기서 epsilon은 hyperparameter이며, 예를 들어 $\epsilon=0.2$로 설정한다. 이 objective의 동기는 다음과 같다. $\min$ 내부의 첫 번째 항은 $L^{CPI}$이다. 두 번째 항인 $\operatorname{clip}(r_t(\theta),1-\epsilon,1+\epsilon)\hat{A}_t$는 probability ratio를 clipping하여 surrogate objective를 수정하며, 이로써 $r_t$를 구간 $[1-\epsilon,1+\epsilon]$ 밖으로 이동시킬 유인을 제거한다. 마지막으로 clipped objective와 unclipped objective 중 최솟값을 취하므로, 최종 objective는 unclipped objective의 lower bound(즉, 비관적 bound)가 된다. 이 방식에서는 probability ratio의 변화가 objective를 개선하는 경우에만 그 변화를 무시하고, objective를 악화시키는 경우에는 이를 반영한다. $\theta_{\mathrm{old}}$ 주위(즉, $r=1$인 지점)에서 first order까지는 $L^{CLIP}(\theta)=L^{CPI}(\theta)$이지만, $\theta$가 $\theta_{\mathrm{old}}$에서 멀어짐에 따라 두 objective는 서로 달라진다. 그림 1은 $L^{CLIP}$의 단일 항(즉, 하나의 $t$에 해당하는 항)을 도시한다. Advantage가 양수인지 음수인지에 따라 probability ratio $r$이 $1-\epsilon$ 또는 $1+\epsilon$에서 clipping됨에 유의한다.

**그림 1:** 양의 advantage(왼쪽)와 음의 advantage(오른쪽)에 대해 probability ratio $r$의 함수로 나타낸 surrogate function $L^{CLIP}$의 한 항(즉, 하나의 timestep)을 보여주는 도표이다. 각 도표의 빨간색 원은 최적화의 시작점, 즉 $r=1$을 나타낸다. $L^{CLIP}$은 이러한 항을 다수 합산한다는 점에 유의한다.

그림 2는 surrogate objective $L^{CLIP}$에 관한 또 다른 직관을 제공한다. Continuous control problem에서 proximal policy optimization(곧 소개할 algorithm)을 통해 얻은 policy update 방향을 따라 interpolation할 때 여러 objective가 어떻게 달라지는지 보여준다. $L^{CLIP}$은 $L^{CPI}$의 lower bound이며, policy update가 지나치게 큰 경우에 대한 penalty를 포함함을 확인할 수 있다.

**그림 2:** 초기 policy parameter $\theta_{\mathrm{old}}$와 PPO를 한 번 iteration한 후 계산한 updated policy parameter 사이를 interpolation할 때의 surrogate objective이다. Updated policy는 initial policy로부터 약 0.02의 KL divergence를 가지며, 이 지점에서 $L^{CLIP}$이 최대가 된다. 이 도표는 6.1절에 제시된 hyperparameter를 사용한 Hopper-v1 문제의 첫 번째 policy update에 해당한다.

## 4 Adaptive KL Penalty Coefficient

Clipped surrogate objective의 대안으로, 또는 그에 더하여 사용할 수 있는 또 다른 접근법은 KL divergence에 penalty를 부과하고, 각 policy update에서 KL divergence가 어떤 target 값 $d_{\mathrm{targ}}$에 도달하도록 penalty coefficient를 조정하는 것이다. 실험에서 KL penalty는 clipped surrogate objective보다 성능이 나빴지만, 중요한 baseline이므로 여기에 포함한다.

이 algorithm의 가장 단순한 형태에서는 각 policy update마다 다음 단계를 수행한다.

- 여러 epoch의 minibatch SGD를 사용하여 다음 KL-penalized objective를 최적화한다.

$$
L^{KLPEN}(\theta)
= \hat{\mathbb{E}}_t\left[
\frac{\pi_\theta(a_t \mid s_t)}{\pi_{\theta_{\mathrm{old}}}(a_t \mid s_t)}\hat{A}_t
- \beta\,\mathrm{KL}\left[\pi_{\theta_{\mathrm{old}}}(\cdot \mid s_t),\pi_\theta(\cdot \mid s_t)\right]
\right]. \tag{8}
$$

- $d=\hat{\mathbb{E}}_t\left[\mathrm{KL}\left[\pi_{\theta_{\mathrm{old}}}(\cdot\mid s_t),\pi_\theta(\cdot\mid s_t)\right]\right]$를 계산한다.
  - $d<d_{\mathrm{targ}}/1.5$이면, $\beta\leftarrow\beta/2$로 설정한다.
  - $d>d_{\mathrm{targ}}\times1.5$이면, $\beta\leftarrow\beta\times2$로 설정한다.

Update된 $\beta$는 다음 policy update에 사용한다. 이 방식을 사용하면 KL divergence가 $d_{\mathrm{targ}}$와 크게 다른 policy update가 간혹 나타나지만, 그러한 경우는 드물며 $\beta$가 빠르게 조정된다. 위의 parameter 1.5와 2는 heuristic하게 선택되었지만 algorithm은 이 값들에 그다지 민감하지 않다. $\beta$의 initial value 역시 또 하나의 hyperparameter이지만, algorithm이 이를 빠르게 조정하므로 실제로는 중요하지 않다.
