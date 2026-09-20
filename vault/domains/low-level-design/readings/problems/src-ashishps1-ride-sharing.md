---
nodes: [problems.marketplaces.ride-sharing]
url: https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/ride-sharing-service.md
---
# awesome-low-level-design — Designing a Ride-Sharing Service Like Uber

值得读：这是这道题最流行的免费题面，八条需求写得很全（叫车、司机接受/拒绝、按邻近匹配、
按里程与时长计价、支付、实时状态通知、并发一致性），拿来核对自己的分关有没有漏项很好用；
六种语言（含 Python）并排给出同一份实体切法 `Passenger` / `Driver` / `Ride` / `Location` /
`Payment` / `RideService`。分歧有三处，都在本题解里被正面回应：它的 `RideService` 用单例，
而本文让服务被构造并注入；它的 `requestRide` 把行程直接挂到最近的司机身上再"通知"对方，
没有要约、没有超时、没有拒单路径——本文认为"司机是被问的，不是被指派的"正是这道题的题眼；
它靠并发容器（ConcurrentHashMap / ConcurrentLinkedQueue）表达线程安全，而真正的竞态是
"先查空闲再写占用"这个复合操作，并发容器对它无能为力，本文用一把锁内的比较并交换解决。
另外它的计价与支付都是占位方法，本文把计价做成可注入的价目表加倍数策略，并说明倍数在下单
那一刻锁死。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/ashishps1/awesome-low-level-design/blob/main/problems/ride-sharing-service.md)

## Archived copy
![[src-ashishps1-ride-sharing-clip]]
%% trellis:end %%
