<!-- src:L1194-L1195 -->
## 논의

<!-- src:L1196-L1200 -->
본 연구의 한계는 균질한 자갈을 적재하는 특정한 경우만을 다루었다는 점이다. 거칠게 파쇄된 암석이나 점착성 토사처럼 더 복잡하고 불균질한 토양을 고려하면 시뮬레이션-현실 격차가 더 커질 가능성이 있다. 반면, [[CITE:Eriksson2023]]의 결과는 다른 재료에 대한 적응이 극복할 수 없는 문제는 아님을 시사한다.

<!-- src:L1202-L1204 -->
본 논문의 휠 로더 모델은 매우 단순화되어 있으며, 특히 엔진과 구동계를 통한 동력 전달, 그리고 붐 리프트 및 버킷 틸트용 유압 계통이 그러하다. 실제로 이들은 동일한 동력원을 공유하며 그 동력을 두고 경쟁한다. 시뮬레이션 시간 간격이나 속도에 영향을 미치지 않는 간단한 모델 확장 방법은 [[CITE:Servin2018]]의 모델을 도입하는 것이다. 그러나 보정해야 할 매개변수의 수는 증가할 것이다.

<!-- src:L1207-L1208 -->
## 결론

<!-- src:L1210-L1220 -->
시뮬레이션-현실 격차가 10\%인 전체 시스템 휠 로딩 시뮬레이터를 구축할 수 있음을 확인하였다. D형 시뮬레이터와 G형 시뮬레이터 사이의 도메인 민감도가 실제 현실 격차를 대표한다면, 이 정도의 시뮬레이션-현실 격차는 최적성을 크게 떨어뜨리지 않고 본 연구에서 검토한 힘 피드백 제어기를 전이하기에 분명히 충분하다. 관찰된 격차는 시뮬레이션 지형의 충실도 수준에 약하게 의존한다. 놀랍게도 축약된 멀티스케일 지형 모델은 자유도와 계산 속도에서 여러 자릿수 규모의 차이가 있음에도 DEM 모델과 같거나 더 우수한 현실성을 제공할 수 있다. 자유 모델 매개변수가 더 많다는 점은 높은 계산 속도로 상쇄되며, 이에 따라 보정 과정에서 훨씬 더 많은 평가를 수행할 수 있다. 연구 결과는 관찰된 시뮬레이션-현실 격차가 수치 오차보다 모델 오차에서 더 많이 기인함을 시사한다. 격차를 더 줄이기 위해서는 엔진, 붐과 버킷의 유압 구동, 그리고 유압 계통과 구동계 사이의 동력 분배를 더욱 정교하게 모델링할 것을 권고한다.

<!-- src:L1224-L1226 -->
## 보충 자료

이 논문의 보충 데이터는 [http://umit.cs.umu.se/wl-sim-to-real/](http://umit.cs.umu.se/wl-sim-to-real/)에서 온라인으로 확인할 수 있다.

<!-- src:L1228-L1230 -->
- **보충 동영상 1**  
  세 가지 버킷 채움 시험 FB35, HD27 및 RD21의 현장 실험과 이에 대응하는 시뮬레이션을 보여준다. 입자 지형 모델과 멀티스케일 지형 모델은 D50(오른쪽 위), G200(왼쪽 아래), G400(오른쪽 아래)이다.

<!-- src:L1231-L1233 -->
- **보충 동영상 2**  
  버킷 채움 시험 FB35, HD27 및 RD21에 대해 서로 다른 여덟 가지 충실도 수준으로 수행한 시뮬레이션을 보여준다. D50/G50(왼쪽 위), D100/G100(오른쪽 위), D200/G200(왼쪽 아래), D400/G400(오른쪽 아래)이다.

<!-- src:L1234-L1236 -->
- **보충 동영상 3**  
  D50 및 G200 시뮬레이터의 영상을 중첩하여 버킷 채움 시험 FB35, HD27 및 RD21의 시뮬레이션을 보여준다. 입자는 속도에 따라 색상으로 구분하였다.

<!-- src:L1237-L1239 -->
- **보충 동영상 4**  
  각 시뮬레이터에서 최적화한 버킷 채움 제어기를 보여준다. D50(왼쪽 위), D100(오른쪽 위), G100(왼쪽 아래), G200(오른쪽 아래)이다. 입자는 속도에 따라 색상으로 구분하였다.

<!-- src:L1243-L1245 -->
## 부록 - 보충 그림

그림~\ref{fig:force_velocity}에는 비교하기 쉽도록 모든 시뮬레이터의 측정값을 하나의 그림에 모았지만, 그 대가로 많은 선이 서로 겹친다. 그림~\ref{fig:suppl-GD50}--\ref{fig:suppl-GD400}에는 각 공간 해상도에 대한 측정값을 제시한다.

<!-- src:L1246-L1255 -->
[[FIGURE label=fig:suppl-GD50 src=fig/force_velocity_sim_FB35_50.pdf,fig/force_velocity_sim_HD27_50.pdf,fig/force_velocity_sim_RD21_50.pdf caption_ko=FB35, HD27, RD21 실험의 시계열과 G50형 및 D50형 시뮬레이터 결과에 대한 속도, 힘, 회전 측정값.]]

<!-- src:L1257-L1266 -->
[[FIGURE label=fig:suppl-GD100 src=fig/force_velocity_sim_FB35_100.pdf,fig/force_velocity_sim_HD27_100.pdf,fig/force_velocity_sim_RD21_100.pdf caption_ko=FB35, HD27, RD21 실험의 시계열과 G100형 및 D100형 시뮬레이터 결과에 대한 속도, 힘, 회전 측정값.]]

<!-- src:L1268-L1277 -->
[[FIGURE label=fig:suppl-GD200 src=fig/force_velocity_sim_FB35_200.pdf,fig/force_velocity_sim_HD27_200.pdf,fig/force_velocity_sim_RD21_200.pdf caption_ko=FB35, HD27, RD21 실험의 시계열과 G200형 및 D200형 시뮬레이터 결과에 대한 속도, 힘, 회전 측정값.]]

<!-- src:L1279-L1288 -->
[[FIGURE label=fig:suppl-GD400 src=fig/force_velocity_sim_FB35_400.pdf,fig/force_velocity_sim_HD27_400.pdf,fig/force_velocity_sim_RD21_400.pdf caption_ko=FB35, HD27, RD21 실험의 시계열과 G400형 및 D400형 시뮬레이터 결과에 대한 속도, 힘, 회전 측정값.]]

<!-- src:L1290-L1291 -->
## 감사의 글

본 연구는 Komatsu Ltd, Algoryx Simulation AB 및 High-Performance Computing Center North(HPC2N)의 Swedish National Infrastructure for Computing으로부터 일부 지원을 받았다.

<!-- src:L1293-L1295 -->
\bibliographystyle{abbrv}
\bibliography{wl_sim2real_gap}
%\bibliography{../../texinputs/digitalphysics}
