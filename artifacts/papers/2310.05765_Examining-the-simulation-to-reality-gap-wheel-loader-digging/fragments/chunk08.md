<!-- src:L1088-L1089 -->
# 7. Force-based control에서의 domain sensitivity와 예측성

<!-- src:L1090-L1100 -->
이 절에서는 자동 버킷 충전을 위한 제어기의 domain sensitivity를 조사한다. 시뮬레이션을 사용하여 제어 파라미터 공간 $\mathcal{A}$를 탐색함으로써 준최적 성능을 내도록 조정할 수 있는 자유 파라미터 $\bm{a} \in \mathcal{A}$를 갖는 제어기를 생각해 보자. 그러면 표적 domain으로 전이할 때 제어 파라미터 선택이 얼마나 민감한지가 관심 대상이 된다. 다시 말해, 시뮬레이션에서 준최적인 것으로 밝혀진 제어 파라미터가 현실에서도 준최적인가? 추가 현장 실험을 수행할 여건은 없었다. 대신 빠른 G200 시뮬레이터로 최적화한 제어기를 D50 시뮬레이터로 전이할 때 나타나는 domain sensitivity를 조사하였다. D50은 훨씬 더 미세하게 해상된 시뮬레이터이며 G200보다 $10^4$배 이상 느리다. 그림~\ref{fig:error_realtimfactor}로부터, 편차의 성격은 다르지만 G200과 D50 사이의 격차가 시뮬레이션-현실 격차와 크기 면에서 유사하다는 것을 알 수 있다.

<!-- src:L1102-L1102 -->
## 7.1. 시험 설정

<!-- src:L1103-L1111 -->
[[CITE:aoshima:2023:pmh]]에서 연구한 것과 동일한 force feedback controller를 자동 버킷 충전에 사용하고 FB35 시험 토사 더미에서 이를 실행하였다. 휠 로더는 토사 더미에서 5 m 떨어진 지점에서 출발하며, 토사 더미를 향해 직진하고 목표 속도는 8 km/h이며 버킷은 지면에 수평으로 낮춘 상태이다. 버킷이 토사 더미에 도달하면 리프트 및 버킷 실린더에 force feedback control 법칙을 적용하여, 버킷 끝단이 토사 더미에서 빠져나올 때까지 버킷을 채운다. 빠져나온 뒤 토사가 가라앉도록 장비를 0.5 s 동안 정지 상태로 유지한 다음, 붐과 버킷의 최종 각도가 각각 $-20^\circ$와 $50^\circ$에 도달하도록 리프트와 틸트를 수행하면서 목표 속도 8 km/h로 후진하기 시작한다. 장비가 출발 지점에 도달하면 적재 사이클이 끝난다.

<!-- src:L1113-L1126 -->
Force feedback controller는 [[CITE:Dobson2017]]의 어드미턴스 제어기를 변형한 것이다. 이 제어기는 붐 및 버킷 실린더용 선형 모터의 목표 속도를 결정한다. 선형 모터는 구속력에 힘 범위 한계를 둔 속도 구속조건으로 모델링된다는 점을 상기하면, 필요한 힘이 모터 한계 이내에 있지 않을 경우 설정한 목표 속도는 실현되지 않는다. 제어기는 다음 목표 속도로 정의한다. 즉, $v_\mathrm{bm}^\text{target} = u_\mathrm{bm}(f_\mathrm{bm},\bm{a}) v_\mathrm{bm}^\text{max}$ 및 $v_\mathrm{bk}^\text{target} = u_\mathrm{bk}(f_\mathrm{bm},\bm{a}) v_\mathrm{bk}^\text{max}$이며, 여기서 $f_\mathrm{bm}$은 적절히 정규화한 붐 실린더의 측정 힘이다. 응답 함수는 $u_\mathrm{bm} = \text{clip}\left(k_\mathrm{bm}\left[f_\mathrm{bm}-\delta_\mathrm{bm}\right],0,1\right)$ 및 $u_\mathrm{bk} = \text{clip}\left(k_\mathrm{bk}\left[f_\mathrm{bm}-\delta_\mathrm{bk}\right],0,1\right)$이며, 여기서 $\text{clip}(value, min, max)$는 $value$를 최솟값과 최댓값 사이로 제한한다. 굴착 저항은 버킷이 토사 더미에 관입하는 깊이에 따라 증가한다. 붐 실린더 힘 $f_\mathrm{bm}$을 통해 관측한 굴착 저항이 임계 파라미터 $\delta_\mathrm{bm}$ 또는 $\delta_\mathrm{bk}$를 초과하면 각각 리프트 또는 틸트 작동이 개시된다. 임계 파라미터의 값이 클수록 일반적으로 더 깊이 관입하는 버킷 trajectory가 형성된다. 이득 파라미터 $k_\mathrm{bm}$과 $k_\mathrm{bk}$는 각각의 반응이 얼마나 빠른지를 조절한다. 이 파라미터들은 제어 파라미터 벡터 $\bm{a} = [\delta_\mathrm{bm}, k_\mathrm{bm}, \delta_\mathrm{bk}, k_\mathrm{bk}]$로 묶인다. 절~\ref{sec:comparison}의 feedforward controller와 달리 적재 사이클을 완료하는 데 걸리는 시간은 전혀 알 수 없으며 제어 파라미터와 토사 더미 형상에 크게 좌우된다는 점에 유의해야 한다.

<!-- src:L1128-L1135 -->
단순화를 위해 여기서는 4차원 제어 파라미터 공간 전체를 다루지 않는다. 대신 $\bm{a}_0 = [0.7, 0.3, 0.2, 0.2]$, $\bm{a}_1 = [0.0, 2.2, 0.15, 4.8]$, 탐색 파라미터 $s \in [0,1]$인 탐색선 $\bm{a}(s) = \bm{a}_0 + (\bm{a}_1-\bm{a}_0)s$를 따라 스윕한다. 일반적으로 $s \approx 0$이면 버킷이 토사 더미에서 빠져나오기 전에 깊이 관입하는 반면, $s \approx 1$이면 표면을 따르는 더 얕은 trajectory가 형성된다. 서로 다른 제어 파라미터를 사용하는 시뮬레이션은 $s$를 $0.0$부터 $1.0$까지 스윕하여 실행하였으며, G200에는 등간격으로 나눈 50개 구간을, D50에는 30개 구간을 사용하였다. 시뮬레이터 충실도 수준에 대한 의존성을 확인하기 위해 G100 및 D100 시뮬레이션도 실행하였다. 예시는 보충 동영상 4에 제시한다.

<!-- src:L1137-L1137 -->
## 7.2. 그 결과 나타나는 domain sensitivity

<!-- src:L1138-L1146 -->
제어 파라미터 및 시뮬레이터에 대해 측정한 적재 질량 $M$, 사이클 시간 $T$, 일 $W$를 그림~\ref{fig:transfer_test_observation}에 나타낸다. 시뮬레이터들은 전반적으로 동일한 의존성을 보이지만 일부 차이도 나타난다. 질량, 시간 및 일은 $s$에 따라 단조 감소하며, 약간의 변동이 있고 그 변동은 D보다 G에서 더 크다. 적재 시간은 잘 일치하며, 버킷 관입이 깊어질 때 시간이 급격히 증가하는 양상을 포착한다. 일의 경우 거의 일정한 50 kJ의 격차가 있으며, G200이 D50보다 약 15\% 큰 값을 산출한다. 질량의 경우 버킷 충전량이 최대인 $s \approx 0$ 영역에서 격차가 25\%이며, $s$가 증가함에 따라 꾸준히 감소한다. 이 격차들은 feedforward control을 사용한 절~\ref{sec:comparison}의 결과와 일치한다. 여기서는 해상도에 대한 의존성이 거의 두드러지지 않는다.

<!-- src:L1148-L1166 -->
[[FIGURE label=fig:transfer_test_observation src=fig/Observation_TransferTest.pdf caption_ko=G200 및 D50 domain에서 force feedback control 파라미터 $s$에 대한 적재 질량 (a), 시간 (b), 일 (c)의 의존성. 해상도에 대한 민감성을 확인하기 위해 G100 및 D100도 함께 나타낸다.]]

<!-- src:L1168-L1173 -->
시뮬레이션한 각 적재 작업의 생산성과 효율은 각각 $M/T$와 $M/W$로 계산한다. 제어 파라미터 및 시뮬레이터 유형에 대한 이들의 의존성을 그림~\ref{fig:domain_sensitivity}에 나타낸다. 앞서 언급한 격차로 인해 생산성의 절댓값은 다르지만 경향은 유사하다. $s$가 0에 가까워짐에 따라 적재 시간이 급격히 증가할 때 생산성도 유사한 양상으로 감소한다. D형 시뮬레이터는 효율이 $s$에 따라 단조 증가한다고 예측하는 반면, G형 시뮬레이터에서는 효율이 대체로 일정하다.

<!-- src:L1175-L1180 -->
[[FIGURE label=fig:domain_sensitivity src=fig/DomainSensitivity_TransferTest.pdf caption_ko=시뮬레이션 domain G100, G200, D50 및 D100에서 파라미터 $\bm{a}(s)$를 사용하는 force feedback control의 domain sensitivity.]]

<!-- src:L1182-L1191 -->
G200 시뮬레이터를 사용하여 최적 제어 파라미터를 선택하고 이를 D50 domain으로 전이하는 것이 과제였다면, 서로 다른 domain에서 domain gap뿐 아니라 최적 파라미터 값의 이동도 경험했을 것이다. 현재 예에서 G200의 최대 생산성은 $s=0.42$에서 약 $416$ kg/s인 반면, D50 시뮬레이션에서 관측한 최대 생산성은 $s=0.36$에서 $366$ kg/s이다. 이는 49 kg/s (13\%)의 domain gap과 0.06의 domain 이동에 해당한다. G200에 최적인 제어 파라미터 $s=0.42$를 D50 domain으로 직접 전이한다면, 확인된 최적값 대비 성능 저하는 2\%에 불과할 것이다. 이는 선택한 행동 공간의 특수한 사례일 수 있으므로, 추가로 10개의 공간에서도 domain sensitivity를 시험하였다. D50의 시뮬레이션 비용을 피하기 위해, 그림~\ref{fig:domain_sensitivity}에 나타난 것처럼 D50과 D100 사이의 격차는 미미하다고 가정하여 추가 시험은 G200과 D100 사이에서 수행하였다. 그 결과 domain gap, domain 이동 및 성능 저하의 평균은 각각 55 kg/s (16\%), 0.22 및 5\%였다.
