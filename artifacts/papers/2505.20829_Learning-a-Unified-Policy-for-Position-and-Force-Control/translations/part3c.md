<!-- source: main.tex lines 655-725 -->

# Force-aware 모방학습 Policy의 세부사항

[[TABLE:tab:rebuttal_il_performance]]

**모방학습 결과(각 task당 50회 trial)**

| Task | `wipe-blackboard` | `open-cabinet` | `close-cabinet` | `open-drawer-occlusion` |
|---|---:|---:|---:|---:|
| **Force 없음** | 0.22 | 0.36 | 0.30 | 0.30 |
| **Force 있음** | 0.58 | 0.70 | 0.72 | 0.76 |

[[FIGURE:fig:open_drawer|fig/open_drawer.pdf|0.8\linewidth]]

**가림이 있는 서랍 열기.** Manipulation 중 gripper가 **가려진다**.

**Task 설정.** 실제 환경에서 hybrid force-position control과 force sensing 능력의 조합이 필요한 네 가지 task를 선정한다.

- `wipe-blackboard` task에서 로봇은 잉크 자국을 효과적으로 제거하기 위해 칠판을 누르면서 측면으로 움직여야 한다. 로봇이 contact를 잃거나 움직이는 동안 충분한 force를 가하지 못하면 잉크가 지워지지 않는다. Position control만 사용하는 접근법은 일관된 contact force를 유지하는 데 어려움을 겪으며, 흔히 contact가 간헐적으로 끊기거나 과도한 force를 가하게 된다. 반면 본 force estimator는 로봇이 안정적인 contact pressure를 지속하도록 하여 효과적으로 닦는 동시에 로봇을 손상할 수 있는 과도한 force의 위험을 최소화한다.
- 눌러서 여는 캐비닛을 사용하는 `open-cabinet` 및 `close-cabinet`의 두 task에서 로봇은 문을 누르기에 충분한 force를 가하여, 문이 튀어나오며 열리거나 닫히게 하는 내장 메커니즘을 작동시켜야 한다. 이전 task와 달리 이 시나리오에서는 작동 중 변위가 미미함에도 로봇이 메커니즘의 저항을 극복하기에 충분한 force를 가해야 한다.
- 반동 메커니즘이 있는 `open-drawer-occlusion` task에서 로봇은 시각적으로 가려진 상태에서 서랍 앞면을 누르기에 충분한 force를 가하여, 서랍이 튀어나오며 열리게 하는 내장 메커니즘을 작동시켜야 한다. 이는 [[REF:fig:open_drawer]]에 나타나 있다.

**평가.** 본 방법과 baseline 간의 정량적 비교를 [[REF:tab:rebuttal_il_performance]]에 제시한다. 구체적으로 다음과 같다.

- `wipe-blackboard` task에서는 로봇이 잉크 자국의 $90\%$를 지우는 것을 성공으로 정의한다. 이 목표를 달성하지 못한 채 제한 시간을 초과하면 실패로 판정한다.
- 반동 메커니즘이 있는 `open-cabinet` 및 `close-cabinet`의 두 task에서는 로봇이 캐비닛 문을 눌러 캐비닛을 열고(또는 닫고), 이후 표면과의 contact를 해제하는 것을 성공으로 정의한다. 로봇이 메커니즘을 작동시키지 못하거나 캐비닛 문을 누른 후 놓지 않으면 실패로 판정한다.
- 반동 메커니즘이 있는 `open-drawer-occlusion` task에서는 로봇이 시각적으로 가려진 상태에서 서랍 앞면을 누른 후 표면과의 contact를 해제하는 것을 성공으로 정의한다. 로봇이 메커니즘을 작동시키지 못하거나 서랍 앞면을 누른 후 놓지 않으면 실패로 판정한다.

[[FIGURE:fig:real_pos_force|fig/y_force_discrete.pdf;fig/z_force_discrete.pdf|0.45\linewidth each]]

**실제 환경 force control 평가.**

# X축 및 Y축 방향의 Force 추정 정확도 평가

Force estimator를 평가하기 위해 5개의 position을 무작위로 선정하고 *X*축을 따라 $-60\,\mathrm{N}$에서 $60\,\mathrm{N}$ 범위의 force를 가한다(본문의 [[REF:fig:imitation]]과 동일함). 또한 Unitree-Z1의 하드웨어 제약으로 인해 *Y*축과 *Z*축에서는 [[REF:fig:real_pos_force]]와 같이 $40\,\mathrm{N}$ 이내에서 추가로 평가한다. Sim-to-real 불일치로 인해 특히 *Y*축에서 부정확한 추정이 발생하지만, 현재 estimator는 본 연구에서 다루는 coarse-grained manipulation task에 충분하다고 본다. 더욱 정밀한 control을 위해 이러한 sim-to-real gap을 줄이는 것은 향후 연구에서 추가로 중점을 둘 방향 중 하나이다.
