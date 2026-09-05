<!-- source: source_layout.txt lines 199–406 -->

# 5 알고리즘

앞 절에서 제시한 surrogate loss들은 일반적인 policy gradient 구현을 약간만 변경하여 계산하고 미분할 수 있다. 자동 미분을 사용하는 구현에서는 단순히 $L^{PG}$ 대신 loss $L^{CLIP}$ 또는 $L^{KLPEN}$을 구성하고, 이 목적함수에 대해 stochastic gradient ascent를 여러 step 수행하면 된다.

분산이 감소된 advantage-function estimator를 계산하는 기법은 대부분 학습된 state-value function $V(s)$를 사용한다. 그 예로 generalized advantage estimation [Sch+15a]이나 [Mni+16]의 finite-horizon estimator가 있다. policy와 value function이 parameter를 공유하는 neural network architecture를 사용하는 경우에는 policy surrogate와 value function error 항을 결합한 loss function을 사용해야 한다. 또한 이전 연구 [Wil92; Mni+16]에서 제안한 것처럼 충분한 exploration을 보장하기 위해 entropy bonus를 추가하여 이 목적함수를 보강할 수 있다. 이 항들을 결합하면 각 iteration에서 (근사적으로) 최대화되는 다음 목적함수를 얻는다.

$$
L_t^{CLIP+VF+S}(\theta)=\hat{\mathbb{E}}_t\left[L_t^{CLIP}(\theta)-c_1L_t^{VF}(\theta)+c_2S[\pi_\theta](s_t)\right]. \tag{9}
$$

여기서 $c_1,c_2$는 coefficient이고, $S$는 entropy bonus를 나타내며, $L_t^{VF}$는 squared-error loss $(V_\theta(s_t)-V_t^{targ})^2$이다.

[Mni+16]을 통해 널리 알려졌으며 recurrent neural network에 사용하기에 적합한 한 가지 policy gradient 구현 방식은 policy를 $T$ timestep 동안 실행하고(여기서 $T$는 episode length보다 훨씬 작다), 수집한 sample로 update를 수행한다. 이 방식에는 timestep $T$ 너머를 참조하지 않는 advantage estimator가 필요하다. [Mni+16]에서 사용한 estimator는 다음과 같다.

$$
\hat{A}_t=-V(s_t)+r_t+\gamma r_{t+1}+\cdots+\gamma^{T-t+1}r_{T-1}+\gamma^{T-t}V(s_T). \tag{10}
$$

여기서 $t$는 주어진 길이 $T$의 trajectory segment 내에서 $[0,T]$에 속하는 time index를 나타낸다. 이 선택을 일반화하면 generalized advantage estimation의 truncated version을 사용할 수 있으며, 이는 $\lambda=1$일 때 식 (10)으로 환원된다.

$$
\hat{A}_t=\delta_t+(\gamma\lambda)\delta_{t+1}+\cdots+(\gamma\lambda)^{T-t+1}\delta_{T-1}, \tag{11}
$$

$$
\text{여기서 }\delta_t=r_t+\gamma V(s_{t+1})-V(s_t). \tag{12}
$$

고정 길이 trajectory segment를 사용하는 proximal policy optimization(PPO) 알고리즘을 아래에 제시한다. 각 iteration에서 $N$개의 (병렬) actor가 각각 $T$ timestep의 데이터를 수집한다. 그런 다음 이 $NT$ timestep의 데이터에 대해 surrogate loss를 구성하고, $K$ epoch 동안 minibatch SGD(또는 대개 더 나은 성능을 내는 Adam [KB14])로 이를 최적화한다.

**알고리즘 1: PPO, Actor-Critic 방식**

```text
for iteration = 1, 2, ... do
    for actor = 1, 2, ..., N do
        환경에서 policy π_{θ_old}를 T timestep 동안 실행한다
        advantage estimate Â_1, ..., Â_T를 계산한다
    end for
    K epoch 및 minibatch size M ≤ NT로 θ에 관해 surrogate L을 최적화한다
    θ_old ← θ
end for
```

# 6 실험

## 6.1 Surrogate Objective 비교

먼저 서로 다른 hyperparameter하에서 몇 가지 surrogate objective를 비교한다. 여기서는 surrogate objective $L^{CLIP}$을 몇 가지 자연스러운 변형 및 ablated version과 비교한다.

- **Clipping 또는 penalty 없음:** $L_t(\theta)=r_t(\theta)\hat{A}_t$
- **Clipping:** $L_t(\theta)=\min\bigl(r_t(\theta)\hat{A}_t,\operatorname{clip}(r_t(\theta),1-\epsilon,1+\epsilon)\hat{A}_t\bigr)$
- **KL penalty (고정 또는 adaptive):** $L_t(\theta)=r_t(\theta)\hat{A}_t-\beta\operatorname{KL}[\pi_{\theta_{old}},\pi_\theta]$

KL penalty에는 고정 penalty coefficient $\beta$를 사용할 수도 있고, Section 4에서 설명한 것처럼 target KL 값 $d_{targ}$를 이용하는 adaptive coefficient를 사용할 수도 있다. log space에서의 clipping도 시도했지만 성능이 더 낫지는 않았다는 점에 유의한다.

각 알고리즘 변형에 대해 hyperparameter를 탐색하므로, 알고리즘을 시험할 benchmark로 계산 비용이 낮은 것을 선택했다. 구체적으로 MuJoCo [TET12] physics engine을 사용하는, OpenAI Gym [Bro+16]에 구현된 simulated robotics task 7개[^2]를 사용했다. 각 task에서 100만 timestep 동안 training을 수행했다. 탐색 대상인 clipping용 hyperparameter($\epsilon$)와 KL penalty용 hyperparameter($\beta,d_{targ}$)를 제외한 나머지 hyperparameter는 Table 3에 제시한다.

policy를 표현하기 위해 64 unit의 hidden layer 두 개와 tanh nonlinearity로 구성된 fully-connected MLP를 사용했으며, [Sch+15b; Dua+16]을 따라 가변 standard deviation을 갖는 Gaussian distribution의 mean을 출력하도록 했다. policy와 value function 사이에 parameter를 공유하지 않았으며(따라서 coefficient $c_1$은 무관하다), entropy bonus도 사용하지 않았다.

각 알고리즘을 7개 environment 모두에서 실행했고, 각 environment마다 random seed 3개를 사용했다. 알고리즘의 각 run은 마지막 100개 episode의 평균 total reward를 계산하여 평가했다. 각 environment에서 random policy가 0점을 받고 최상의 결과가 1점이 되도록 score를 shift 및 scale한 뒤, 21개 run에 걸쳐 평균하여 각 알고리즘 설정마다 하나의 scalar를 산출했다.

결과는 Table 1에 제시한다. clipping이나 penalty가 없는 설정에서는 score가 음수임에 유의한다. 한 environment(half cheetah)에서 매우 큰 음의 score가 발생하여 초기 random policy보다도 나쁜 결과를 내기 때문이다.

| 알고리즘 | 평균 normalized score |
|---|---:|
| Clipping 또는 penalty 없음 | -0.39 |
| Clipping, $\epsilon=0.1$ | 0.76 |
| Clipping, $\epsilon=0.2$ | 0.82 |
| Clipping, $\epsilon=0.3$ | 0.70 |
| Adaptive KL $d_{targ}=0.003$ | 0.68 |
| Adaptive KL $d_{targ}=0.01$ | 0.74 |
| Adaptive KL $d_{targ}=0.03$ | 0.71 |
| Fixed KL, $\beta=0.3$ | 0.62 |
| Fixed KL, $\beta=1.$ | 0.71 |
| Fixed KL, $\beta=3.$ | 0.72 |
| Fixed KL, $\beta=10.$ | 0.69 |

**Table 1:** continuous control benchmark의 결과. 각 알고리즘/hyperparameter 설정에 대한 평균 normalized score(7개 environment에서 수행한 알고리즘의 21개 run에 걸친 평균)이다. $\beta$는 1로 초기화했다.

## 6.2 Continuous Domain에서 다른 알고리즘과의 비교

다음으로 PPO(Section 3의 “clipped” surrogate objective 사용)를 문헌에서 continuous problem에 효과적인 것으로 여겨지는 몇 가지 다른 방법과 비교한다. 다음 알고리즘들의 tuning된 구현을 비교 대상으로 삼았다. trust region policy optimization [Sch+15b], cross-entropy method(CEM) [SL06], adaptive stepsize를 사용하는 vanilla policy gradient[^3], A2C [Mni+16], trust region을 사용하는 A2C [Wan+16]이다. A2C는 advantage actor critic을 뜻하며 A3C의 synchronous version이다. 실험 결과 synchronous version은 asynchronous version과 성능이 같거나 더 우수했다. PPO에는 이전 절의 hyperparameter를 $\epsilon=0.2$로 설정해 사용했다. 거의 모든 continuous control environment에서 PPO가 기존 방법보다 우수한 성능을 보임을 확인할 수 있다.

**Figure 3의 그래프 제목:** HalfCheetah-v1; Hopper-v1; InvertedDoublePendulum-v1; InvertedPendulum-v1; Reacher-v1; Swimmer-v1; Walker2d-v1
**Legend:** A2C; A2C + Trust Region; CEM; PPO (Clip); Vanilla PG, Adaptive; TRPO

**Figure 3:** 여러 MuJoCo environment에서 100만 timestep 동안 training한 여러 알고리즘의 비교.

[^2]: HalfCheetah, Hopper, InvertedDoublePendulum, InvertedPendulum, Reacher, Swimmer, Walker2d이며, 모두 “-v1”이다.

[^3]: 각 data batch 후 original policy와 updated policy 간 KL divergence에 따라 Adam stepsize를 조정하며, Section 4에 제시된 것과 유사한 rule을 사용한다. 구현은 <https://github.com/berkeleydeeprlcourse/homework/tree/master/hw4>에서 확인할 수 있다.

## 6.3 Continuous Domain의 시연: Humanoid Running 및 Steering

고차원 continuous control problem에서 PPO의 성능을 보여주기 위해, robot이 달리고 방향을 조절하고 바닥에서 일어나야 하며 때로는 cube 세례까지 견뎌야 하는 3D humanoid 관련 problem set을 학습한다. 시험하는 세 task는 다음과 같다. (1) RoboschoolHumanoid: 전진 locomotion만 수행한다. (2) RoboschoolHumanoidFlagrun: 200 timestep마다 또는 goal에 도달할 때마다 target의 position이 무작위로 바뀐다. (3) RoboschoolHumanoidFlagrunHarder: robot이 cube 세례를 받으며 바닥에서 일어나야 한다. 학습된 policy의 정지 frame은 Figure 5를, 세 task의 learning curve는 Figure 4를 참조한다. Hyperparameter는 Table 4에 제시한다. 동시에 수행된 연구에서 Heess 등 [Hee+17]은 3D robot의 locomotion policy를 학습하기 위해 PPO의 adaptive KL variant(Section 4)를 사용했다.

**Figure 4의 그래프 제목:** RoboschoolHumanoid-v0; RoboschoolHumanoidFlagrun-v0; RoboschoolHumanoidFlagrunHarder-v0
**축 이름:** Timestep

**Figure 4:** Roboschool을 사용한 3D humanoid control task에서 PPO의 learning curve.

**Figure 5:** RoboschoolHumanoidFlagrun으로부터 학습된 policy의 정지 frame. 처음 여섯 frame에서 robot은 target을 향해 달린다. 이후 target의 position이 무작위로 바뀌면, robot은 방향을 틀어 새로운 target을 향해 달린다.

## 6.4 Atari Domain에서 다른 알고리즘과의 비교

Arcade Learning Environment [Bel+15] benchmark에서도 PPO를 실행하고, 충분히 tuning된 A2C [Mni+16] 및 ACER [Wan+16] 구현과 비교했다. 세 알고리즘 모두 [Mni+16]에서 사용한 것과 동일한 policy network architecture를 사용했다. PPO의 hyperparameter는 Table 5에 제시한다. 다른 두 알고리즘에는 이 benchmark에서 성능을 최대화하도록 tuning한 hyperparameter를 사용했다.

49개 game 전체의 결과 표와 learning curve는 Appendix B에 제시한다. 다음 두 scoring metric을 고려한다. (1) 전체 training period에 걸친 episode당 average reward(빠른 학습에 유리함), (2) training의 마지막 100개 episode에 걸친 episode당 average reward(최종 성능에 유리함). Table 2는 각 알고리즘이 “승리한” game 수를 보여주며, 세 번의 trial에 걸쳐 scoring metric을 평균하여 승자를 결정했다.

| scoring metric | A2C | ACER | PPO | Tie |
|---|---:|---:|---:|---:|
| (1) 전체 training에 걸친 평균 episode reward | 1 | 18 | 30 | 0 |
| (2) 마지막 100개 episode에 걸친 평균 episode reward | 1 | 28 | 19 | 1 |

**Table 2:** 각 알고리즘이 “승리한” game 수. scoring metric은 세 번의 trial에 걸쳐 평균했다.