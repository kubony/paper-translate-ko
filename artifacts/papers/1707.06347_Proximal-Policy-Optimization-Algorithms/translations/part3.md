<!-- source lines: 410–672 -->

## 7 결론

우리는 각 정책 갱신을 수행하기 위해 여러 에포크의 확률적 경사 상승을 사용하는 정책 최적화 방법군인 근접 정책 최적화(proximal policy optimization)를 소개하였다. 이 방법들은 신뢰 영역 방법의 안정성과 신뢰성을 갖추면서도 구현이 훨씬 간단하여, 기본적인 정책 경사 구현에서 코드 몇 줄만 변경하면 된다. 또한 더 일반적인 설정(예를 들어 정책과 가치 함수에 공동 아키텍처를 사용하는 경우)에 적용할 수 있으며, 전반적인 성능도 더 우수하다.

## 8 감사의 말

통찰력 있는 의견을 제공해 준 Rocky Duan, Peter Chen 및 OpenAI의 다른 구성원들에게 감사한다.

## 참고문헌

[Bel+15] M. Bellemare, Y. Naddaf, J. Veness, and M. Bowling. “The arcade learning environment: An evaluation platform for general agents”. In: *Twenty-Fourth International Joint Conference on Artificial Intelligence*. 2015.

[Bro+16] G. Brockman, V. Cheung, L. Pettersson, J. Schneider, J. Schulman, J. Tang, and W. Zaremba. “OpenAI Gym”. In: *arXiv preprint arXiv:1606.01540* (2016).

[Dua+16] Y. Duan, X. Chen, R. Houthooft, J. Schulman, and P. Abbeel. “Benchmarking Deep Reinforcement Learning for Continuous Control”. In: *arXiv preprint arXiv:1604.06778* (2016).

[Hee+17] N. Heess, S. Sriram, J. Lemmon, J. Merel, G. Wayne, Y. Tassa, T. Erez, Z. Wang, A. Eslami, M. Riedmiller, et al. “Emergence of Locomotion Behaviours in Rich Environments”. In: *arXiv preprint arXiv:1707.02286* (2017).

[KL02] S. Kakade and J. Langford. “Approximately optimal approximate reinforcement learning”. In: *ICML*. Vol. 2. 2002, pp. 267–274.

[KB14] D. Kingma and J. Ba. “Adam: A method for stochastic optimization”. In: *arXiv preprint arXiv:1412.6980* (2014).

[Mni+15] V. Mnih, K. Kavukcuoglu, D. Silver, A. A. Rusu, J. Veness, M. G. Bellemare, A. Graves, M. Riedmiller, A. K. Fidjeland, G. Ostrovski, et al. “Human-level control through deep reinforcement learning”. In: *Nature* 518.7540 (2015), pp. 529–533.

[Mni+16] V. Mnih, A. P. Badia, M. Mirza, A. Graves, T. P. Lillicrap, T. Harley, D. Silver, and K. Kavukcuoglu. “Asynchronous methods for deep reinforcement learning”. In: *arXiv preprint arXiv:1602.01783* (2016).

[Sch+15a] J. Schulman, P. Moritz, S. Levine, M. Jordan, and P. Abbeel. “High-dimensional continuous control using generalized advantage estimation”. In: *arXiv preprint arXiv:1506.02438* (2015).

[Sch+15b] J. Schulman, S. Levine, P. Moritz, M. I. Jordan, and P. Abbeel. “Trust region policy optimization”. In: *CoRR, abs/1502.05477* (2015).

[SL06] I. Szita and A. Lőrincz. “Learning Tetris using the noisy cross-entropy method”. In: *Neural computation* 18.12 (2006), pp. 2936–2941.

[TET12] E. Todorov, T. Erez, and Y. Tassa. “MuJoCo: A physics engine for model-based control”. In: *Intelligent Robots and Systems (IROS), 2012 IEEE/RSJ International Conference on*. IEEE. 2012, pp. 5026–5033.

[Wan+16] Z. Wang, V. Bapst, N. Heess, V. Mnih, R. Munos, K. Kavukcuoglu, and N. de Freitas. “Sample Efficient Actor-Critic with Experience Replay”. In: *arXiv preprint arXiv:1611.01224* (2016).

[Wil92] R. J. Williams. “Simple statistical gradient-following algorithms for connectionist reinforcement learning”. In: *Machine learning* 8.3-4 (1992), pp. 229–256.

## A 하이퍼파라미터

| 하이퍼파라미터 | 값 |
|---|---:|
| 지평선 ($T$) | 2048 |
| Adam 스텝 크기 | $3 \times 10^{-4}$ |
| 에포크 수 | 10 |
| 미니배치 크기 | 64 |
| 할인율 ($\gamma$) | 0.99 |
| GAE 파라미터 ($\lambda$) | 0.95 |

**표 3:** Mujoco 100만 타임스텝 벤치마크에 사용한 PPO 하이퍼파라미터.

| 하이퍼파라미터 | 값 |
|---|---:|
| 지평선 ($T$) | 512 |
| Adam 스텝 크기 | $*$ |
| 에포크 수 | 15 |
| 미니배치 크기 | 4096 |
| 할인율 ($\gamma$) | 0.99 |
| GAE 파라미터 ($\lambda$) | 0.95 |
| 액터 수 | 32 (locomotion), 128 (flagrun) |
| 행동 분포의 로그 표준편차 | $\operatorname{LinearAnneal}(-0.7, -1.6)$ |

**표 4:** Roboschool 실험에 사용한 PPO 하이퍼파라미터. Adam 스텝 크기는 KL 발산의 목표값에 따라 조정하였다.

| 하이퍼파라미터 | 값 |
|---|---:|
| 지평선 ($T$) | 128 |
| Adam 스텝 크기 | $2.5 \times 10^{-4} \times \alpha$ |
| 에포크 수 | 3 |
| 미니배치 크기 | $32 \times 8$ |
| 할인율 ($\gamma$) | 0.99 |
| GAE 파라미터 ($\lambda$) | 0.95 |
| 액터 수 | 8 |
| 클리핑 파라미터 $\epsilon$ | $0.1 \times \alpha$ |
| VF 계수 $c_1$ (9) | 1 |
| 엔트로피 계수 $c_2$ (9) | 0.01 |

**표 5:** Atari 실험에 사용한 PPO 하이퍼파라미터. $\alpha$는 학습 과정에 걸쳐 1에서 0까지 선형적으로 어닐링된다.

## B 더 많은 Atari 게임에서의 성능

여기서는 49개 Atari 게임으로 이루어진 더 큰 모음에서 PPO와 A2C를 비교한다. 그림 6은 세 개 난수 시드 각각의 학습 곡선을 보여 주며, 표 6은 평균 성능을 보여 준다.

그림 안의 게임명, 축 눈금 및 범례는 다음과 같다(Atari 게임명은 원문 그대로 유지하였다).

```text
                           Alien                           Amidar                           Assault                            Asterix                        Asteroids

           2000                               750                                                              7500                                  2500
                                                                               4000
                                              500                                                              5000                                  2000
           1000                               250                              2000                            2500                                  1500
                                                0                                 0                              0
                          Atlantis                        BankHeist                        BattleZone                        BeamRider                         Bowling
                                                                              20000                            4000
         3000000                              1000                            15000                                                                    50
                                                                                                               3000
         2000000                                                                                                                                       40
                                              500                             10000                            2000
         1000000                                                                                                                                       30
                                                                               5000                            1000
              0                                 0
                          Boxing                          Breakout                         Centipede                      ChopperCommand                    CrazyClimber
            100
                                              400                                                              6000
                                                                              10000
                                                                                                                                                   100000
             50                               200                                                              4000
                                                                               5000                                                                 50000
                                                                                                               2000
              0                                 0
                        DemonAttack                      DoubleDunk                          Enduro                         FishingDerby                      Freeway
          40000                               10.0                              750                                                                    30
                                              12.5                                                               0
                                                                                500                                                                    20
          20000
                                              15.0                                                              50
                                                                                250                                                                    10
                                              17.5
              0                                                                   0                            100                                      0
                         Frostbite                         Gopher                           Gravitar                         IceHockey                       Jamesbond
            300                                                                                                  4
                                                                                                                                                      600
                                             40000                              750                              6
                                                                                                                                                      400
            200                              20000                              500                              8
                                                                                                                                                      200
                                                                                250                             10
            100                                 0                                                                                                       0
                         Kangaroo                           Krull                         KungFuMaster                    MontezumaRevenge                   MsPacman
                                                                              40000                             100
                                              8000                                                                                                   3000
          10000
                                              6000                            20000                                                                  2000
                                                                                                                50
           5000                               4000                                                                                                   1000
              0                               2000                                0                              0
                       NameThisGame                         Pitfall                          Pong                            PrivateEye                         Qbert
                                                0                                20                                                                 15000
          10000
           7500                                                                                                 500                                 10000
                                              100                                 0
           5000                                                                                                                                      5000
                                                                                                                 0
           2500                                                                 20                                                                      0
                         Riverraid                       RoadRunner                         Robotank                          Seaquest                      SpaceInvaders
          10000                                                                   6
                                             40000                                                             1500
           7500                                                                                                                                      1000
                                                                                  4                            1000
           5000                              20000
                                                                                                                500                                   500
           2500
                                                0                                 2
                                                                                                                 0
                        StarGunner                         Tennis                           TimePilot                        Tutankham                        UpNDown
                                                                                                                300                                200000
          40000                                10
                                                                               4000                             200
                                               15                                                                                                  100000
          20000
                                               20                                                               100
                                                                               3000
              0                                                                                                  0                                      0
                          Venture                        VideoPinball                     WizardOfWor                          Zaxxon
                                            150000                                                             6000                                                       A2C
             10                                                                4000
                                                                                                               4000                                                       ACER
                                            100000
              5                                                                2000                            2000
                                                                                                                                                                          PPO
                                             50000
              0                                                                                                  0
                   0                  40M            0                  40M           0                  40M          0                      40M
                         프레임                           프레임                            프레임                            프레임
```

**그림 6:** 출판 당시 OpenAI Gym에 포함되어 있던 49개 ATARI 게임 전체에서 PPO와 A2C를 비교한 결과.

| 게임 | A2C | ACER | PPO |
|---|---:|---:|---:|
| Alien | 1141.7 | 1655.4 | 1850.3 |
| Amidar | 380.8 | 827.6 | 674.6 |
| Assault | 1562.9 | 4653.8 | 4971.9 |
| Asterix | 3176.3 | 6801.2 | 4532.5 |
| Asteroids | 1653.3 | 2389.3 | 2097.5 |
| Atlantis | 729265.3 | 1841376.0 | 2311815.0 |
| BankHeist | 1095.3 | 1177.5 | 1280.6 |
| BattleZone | 3080.0 | 8983.3 | 17366.7 |
| BeamRider | 3031.7 | 3863.3 | 1590.0 |
| Bowling | 30.1 | 33.3 | 40.1 |
| Boxing | 17.7 | 98.9 | 94.6 |
| Breakout | 303.0 | 456.4 | 274.8 |
| Centipede | 3496.5 | 8904.8 | 4386.4 |
| ChopperCommand | 1171.7 | 5287.7 | 3516.3 |
| CrazyClimber | 107770.0 | 132461.0 | 110202.0 |
| DemonAttack | 6639.1 | 38808.3 | 11378.4 |
| DoubleDunk | -16.2 | -13.2 | -14.9 |
| Enduro | 0.0 | 0.0 | 758.3 |
| FishingDerby | 20.6 | 34.7 | 17.8 |
| Freeway | 0.0 | 0.0 | 32.5 |
| Frostbite | 261.8 | 285.6 | 314.2 |
| Gopher | 1500.9 | 37802.3 | 2932.9 |
| Gravitar | 194.0 | 225.3 | 737.2 |
| IceHockey | -6.4 | -5.9 | -4.2 |
| Jamesbond | 52.3 | 261.8 | 560.7 |
| Kangaroo | 45.3 | 50.0 | 9928.7 |
| Krull | 8367.4 | 7268.4 | 7942.3 |
| KungFuMaster | 24900.3 | 27599.3 | 23310.3 |
| MontezumaRevenge | 0.0 | 0.3 | 42.0 |
| MsPacman | 1626.9 | 2718.5 | 2096.5 |
| NameThisGame | 5961.2 | 8488.0 | 6254.9 |
| Pitfall | -55.0 | -16.9 | -32.9 |
| Pong | 19.7 | 20.7 | 20.7 |
| PrivateEye | 91.3 | 182.0 | 69.5 |
| Qbert | 10065.7 | 15316.6 | 14293.3 |
| Riverraid | 7653.5 | 9125.1 | 8393.6 |
| RoadRunner | 32810.0 | 35466.0 | 25076.0 |
| Robotank | 2.2 | 2.5 | 5.5 |
| Seaquest | 1714.3 | 1739.5 | 1204.5 |
| SpaceInvaders | 744.5 | 1213.9 | 942.5 |
| StarGunner | 26204.0 | 49817.7 | 32689.0 |
| Tennis | -22.2 | -17.6 | -14.8 |
| TimePilot | 2898.0 | 4175.7 | 4342.0 |
| Tutankham | 206.8 | 280.8 | 254.4 |
| UpNDown | 17369.8 | 145051.4 | 95445.0 |
| Venture | 0.0 | 0.0 | 0.0 |
| VideoPinball | 19735.9 | 156225.6 | 37389.0 |
| WizardOfWor | 859.0 | 2308.3 | 4185.3 |
| Zaxxon | 16.3 | 29.0 | 5008.7 |

**표 6:** 4천만 게임 프레임(1천만 타임스텝) 후 Atari 게임에서 PPO와 A2C가 기록한 최종 점수(마지막 100개 에피소드)의 평균.
