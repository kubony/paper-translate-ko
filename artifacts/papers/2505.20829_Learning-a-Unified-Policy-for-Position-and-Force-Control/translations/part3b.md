<!-- source: main.tex lines 558-654 -->

## Reward 및 Domain Randomization

[[REF:tab:method:rewards]]는 본 연구에서 사용한 reward 구조를 상세히 개괄하며, [[REF:tab:method:radomization]]는 채택한 domain randomization 방식을 제시한다.

[[TABLE:tab:method:rewards]]

**표: Whole-body policy 학습을 위한 reward 항.**

| *항* | *수식* | *가중치* |
|---|---|---:|
| **End-effector 통합 Position 및 Force Control** |  |  |
| Gripper position | `exp(−‖x_ee − [x_cmd + (F_ext + F_cmd − F_react)/B]‖ / 0.5)` | $2.0$ |
| **Base 통합 Position 및 Force Control ($\mathbf{r}_v^b$)** |  |  |
| Base velocity | `exp(−‖v_base − [v_base,cmd + F_base/D]‖ / 0.25)` | $2.0$ |
| **안전성 및 Smoothness** |  |  |
| Collision penalty | $\mathbb{1}_{\mathrm{collision}}$ | $-5.0$ |
| Joint limit | $\mathbb{1}_{q>0.8*q^{\max}\;\|\|\;q<0.8*q^{\min}}$ | $-10.0$ |
| Torque | $\lvert\boldsymbol{\tau}\rvert^2$ | $-5\mathrm{e}{-6}$ |
| Joint velocity | $\lvert\dot{q}\rvert^2$ | $-8\mathrm{e}{-4}$ |
| Joint acceleration | $\lvert\ddot{q}\rvert^2$ | $-2\mathrm{e}{-7}$ |
| Action rate | $\lvert a_{t-1}-a_t\rvert$ | $-0.02$ |
| Torque limit | $\mathbb{1}_{\boldsymbol{\tau}>0.9*\lvert\boldsymbol{\tau}^{\max}\rvert}$ | $-0.005$ |
| **Gait** |  |  |
| Contact number | $\sum_{\mathrm{foot}}\mathbb{1}_{\boldsymbol{\tau}_{\mathrm{contact}}>5.}*\mathrm{stance\_mask}$ | $2.0$ |
| Reference motion | $\lvert q-q^{\mathrm{ref}}\rvert^2$ | $1.0$ |

[[TABLE:tab:method:radomization]]

**표: Whole-body policy 학습을 위한 domain randomization.**

| *항* | *단위* | *범위* |
|---|---:|---|
| Friction | - | $[0.3,\,2.0]$ |
| Body mass | kg | $[0.0,\,15.0]$ |
| Base COM (x, y, z축) | m | $[-0.15,\,0.15]$ |
| Motor strength | % | $[85,\,115]$ |
| Gripper payload | kg | $[0.0,\,0.5]$ |
| Robot 밀기 | m/s | $[0.0,\,0.8]$, interval = 8 s |

## 월드 정렬 End-Effector Position 추정

본 estimator는 외력뿐만 아니라 end-effector position과 base linear velocity도 예측한다. Forward kinematics는 arm base에 대한 end-effector의 상대 position을 제공하지만, arm control을 base posture로부터 분리한다. 이와 달리 본 연구에서는 월드 정렬 base frame, 즉 base projection에 대해 height와 orientation이 고정된 frame에서 end-effector position을 추정한다. 예를 들어 이 표현을 사용하면 아래쪽을 향하는 end-effector 명령이 workspace 한계 근처에서 자연스럽게 robot base의 기울어짐을 유발하므로, 명시적인 base control 없이도 조율된 whole-body 동작이 가능하다. 이 frame에서의 end-effector position은 직접 측정할 수 없으므로 대신 이를 추정한다.

## Policy 학습에 관한 추가 분석

[[FIGURE:fig:reward_curve|fig/reward.pdf|1.0\linewidth]]

**그림: 학습 reward 곡선(확대 보기 포함).**

학습 초기에 외부 외란을 도입하면 초기 policy가 body balance와 end-effector 안정성을 유지하는 데 어려움을 겪기 때문에 학습이 까다로워진다. 이를 해결하기 위해 2단계 curriculum을 사용했다. 먼저 whole-body reaching과 locomotion을 학습한 다음, 무작위 force 명령과 외란을 추가했다. 학습 reward 곡선([[REF:fig:reward_curve]])은 2단계 초기에 reward가 하락하지만 이후 locomotion은 회복되고 whole-body reaching은 안정화됨을 보여준다. 다만 force 명령과 외란의 sampling 다양성이 증가함에 따라 reaching reward는 소폭 감소한다.

## Motor Gain의 영향

순수한 position 기반 whole-body control과 비교하여 본 연구에서는 더 작은 Kp/Kd gain을 사용한다. 더 큰 overshoot를 허용하는 낮은 gain이 force 추정을 향상한다는 것을 관찰했다. 그러나 값이 지나치게 낮으면 position tracking 정확도가 저하된다.

## Sim-to-Real Gap 및 Force 추정 Robustness

본 force estimator에는 motor dynamics와 contact modeling의 불일치로 인한 sim2real gap이 발생한다. Domain randomization(예: Kp/Kd gain 변화)이 이러한 gap을 줄이는 데 도움이 되지만, RL 기반 policy의 sim2real transfer는 여전히 어렵다. Contact가 많은 task에서 인간이 정밀한 force sensing보다 tactile feedback에 더 의존한다는 점에서 착안하여, 본 IL policy는 추정 force와 visual input을 결합함으로써 높은 force 정확도를 요구하지 않고도 robust한 성능을 달성한다. Sim2real gap을 더욱 줄이기 위해 향후 real-world data로 estimator를 fine-tuning하고 system identification 방법을 적용할 계획이다.
