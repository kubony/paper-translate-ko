<!-- src:L975-L976 -->
## 6.4. 스칼라 시계열

<!-- src:L978-L991 -->
그림~\ref{fig:force_velocity}에 제시한 스칼라 시계열 측정값을 살펴보면, 주행 속도와 버킷 및 붐의 회전은 시뮬레이션과 실험 간에 상당히 잘 일치한다. G400 시뮬레이터의 편차가 가장 크다는 점이 두드러진다. 견인력 MAE(표~\ref{table:sim-to-real_error_granular} 및 \ref{table:sim-to-real_error_terrain}의 $\mathcal{E}_\mathrm{tr}$)는 8\%에서 19\% 사이이며, 주행 장치, 붐 및 버킷을 동시에 작동할 때(HD27 및 RD21) 오차가 가장 크다. 시뮬레이션된 붐 리프트력과 버킷 틸트력의 추세는 실험에서 측정한 추세와 일치하지만, 때때로 상당한 편차가 나타난다. 리프트력과 틸트력의 편차는 FB35 시험에서는 약 $7$ s, RD21 시험에서는 약 $14$ s의 돌파 시점에 가장 크지만, 약 $8$ s에 돌파가 발생하는 HD27 시험에서는 그렇지 않다. 돌파 후에는 시뮬레이션과 실제 리프트력이 잘 일치하며, 이는 버킷이 기계적 끝점에 도달하여 힘이 재분배되는 시점까지 버킷 채움이 잘 일치함을 나타낸다. 이 현상은 FB35에서는 약 $10$ s, RD21에서는 약 $14.5$ s에 발생한다.

<!-- src:L993-L996 -->
평균적으로 리프트력과 틸트력의 오차(표~\ref{table:sim-to-real_error_granular} 및 \ref{table:sim-to-real_error_terrain}의 $\mathcal{E}_\mathrm{l}$ 및 $\mathcal{E}_\mathrm{t}$)는 모두 평균 11\%이며, D400과 D200의 경우를 제외하면 D형 시뮬레이터가 G형 시뮬레이터보다 약간 작다. 차체 각도의 상대 오차는 크고 가장 거친 시뮬레이터에서 최대이지만, 절댓값으로는 작다. 가능한 원인은 타이어 압력의 모델 오차이거나, 시뮬레이션에서는 평탄하다고 가정한 지면이 완전히 평탄하지 않았기 때문일 수 있다.

<!-- src:L998-L1010 -->
[[FIGURE label=fig:force_velocity src=fig/trajectory_legend.pdf,fig/force_velocity_sim_FB35.pdf,fig/force_velocity_sim_HD27.pdf,fig/force_velocity_sim_RD21.pdf caption_ko=FB35, HD27 및 RD21 실험(검은색 파선)과 G형(파란색) 및 D형(빨간색) 시뮬레이터의 속도, 힘 및 회전 시계열 측정값. 비교는 음영이 없는 구간에서 수행하며, 초기화 단계와 돌파 후 후진 단계는 제외한다. 개별 플롯은 부록~\ref{sec:supplemental_fig}에 제시한다.]]

<!-- src:L1012-L1013 -->
## 6.5. 적재 질량과 일

<!-- src:L1014-L1022 -->
적재 질량과 일의 상대 오차는 표~\ref{table:sim-to-real_error_granular} 및 \ref{table:sim-to-real_error_terrain}에 열거한다. D형 시뮬레이터에서는 적재 질량을 과소평가하며 평균 오차는 15\%이고, G형 시뮬레이터에서는 대부분 과대평가하며 평균 오차는 12\%이다. 누적 일의 경우 각각의 평균 오차는 17\%와 21\%이다. 마찬가지로 D형 시뮬레이터는 대부분 일을 과소평가하는 반면, G형 시뮬레이터는 대부분 과대평가한다. 그림~\ref{fig:work}에는 주행, 리프트 및 틸트 작동이 각각 기여하는 동력 소비의 시계열 예를 제시한다. 동력은 주행에 가장 많이 소비되고, 그다음으로 틸트에 많이 소비된다. 두 시뮬레이터 유형 모두 현장 시험과 유사한 동력 소비 추세를 보인다.

<!-- src:L1024-L1048 -->
[[FIGURE label=fig:work src=fig/W_FB35.pdf,fig/W_HD27.pdf,fig/W_RD21.pdf,fig/W_FB35-D50.pdf,fig/W_HD27-D50.pdf,fig/W_RD21-D50.pdf,fig/W_FB35-G200.pdf,fig/W_HD27-G200.pdf,fig/W_RD21-G200.pdf caption_ko=세 시험의 동력 소비 시계열과 D50 및 G200 시뮬레이터에서 얻은 결과 예. 주행, 리프트 및 틸트 액추에이터가 총 일에 기여하는 양을 제시한다.]]

<!-- src:L1050-L1051 -->
## 6.6. Sim-to-real 오차와 시뮬레이션 속도

<!-- src:L1052-L1059 -->
각 시험과 시뮬레이터 충실도에 대한 평균 오차를 계산하였다. 이 값들은 표~\ref{table:sim-to-real_error_granular} 및 \ref{table:sim-to-real_error_terrain}의 맨 오른쪽 열에 열거하고 그림~\ref{fig:error_realtimfactor}(a)에 도시하였다. 이 값은 시뮬레이터의 현실 격차를 포착하기 위한 것이므로 이를 *sim-to-real 오차*라고 지칭한다. 전체적으로 sim-to-real 오차는 약 10\%이고 표준편차는 3\%이다. 평균적으로 sim-to-real 오차는 해상도 척도(격자 및 입자 크기)가 커질수록 증가한다. G50의 경우를 제외하면 G형 시뮬레이터의 오차가 D형 시뮬레이터보다 다소 작다.

<!-- src:L1061-L1065 -->
각 시뮬레이터를 현장 시험과 비교하지 않고 충실도가 가장 높은 시뮬레이터인 D50과 비교하면 그림~\ref{fig:error_realtimfactor}(b)의 평균 *sim-to-sim 오차*를 얻는다. D형 시뮬레이터의 sim-to-sim 오차는 입자 크기에 따라 증가하는데, 이는 자기 일관성 오차이므로 예상할 수 있는 결과이다. 반면 G50–G400 시뮬레이터는 D50과 비교할 때 평균 15\%의 오차만큼 차이가 난다.

<!-- src:L1067-L1074 -->
표~\ref{table:simulators}에 열거한 서로 다른 시간 간격, 입자 수 및 솔버 반복 횟수가 보여 주듯이, 시뮬레이터마다 계산 집약도와 속도가 크게 다르다. 실시간 계수(계산 시간을 시뮬레이션 시간으로 나눈 값)는 단일 Intel i7-8700K 3.70 GHz 프로세서를 탑재한 워크스테이션을 사용하여 측정하였다. 그 결과를 그림~\ref{fig:error_realtimfactor}(c)에 제시한다. G형 시뮬레이터는 동일한 해상도의 D형 시뮬레이터보다 대략 100배 빠르며, G200은 실시간으로 실행되고 G400은 실시간보다 5배 빠르게 실행된다. G200 시뮬레이터는 sim-to-real 오차와 속도 간 절충에서 최적점으로 간주할 수 있다.

<!-- src:L1076-L1084 -->
[[FIGURE label=fig:error_realtimfactor src=fig/sim-to-real_error.pdf,fig/sim-to-sim_error.pdf,fig/realtimefactor.pdf caption_ko=서로 다른 시뮬레이터 충실도 수준에 대한 sim-to-real 오차, sim-to-sim 오차 및 실시간 계수. 실선은 세 시험의 평균이고, 음영 영역은 표준편차를 나타낸다. 공간 해상도는 입자 크기와 격자 셀 크기를 가리킨다.]]
