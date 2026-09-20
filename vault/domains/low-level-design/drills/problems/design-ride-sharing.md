---
nodes: [problems.marketplaces.ride-sharing, patterns.strategy, structure.state-machines]
tags: [problem]
---
# Drill：网约车（Ride Sharing / Uber）

一个像 Uber 那样的叫车系统：乘客发起叫车，系统给他找一位司机，行程要能跟踪状态，结束时算钱。
一个城市里同时有几千位在线司机、每秒几十次叫车。**地图不在这道题里**——坐标是平面点，距离是
直线距离，邻近搜索是另一道完整的题。金额一律是整数最小货币单位（分）。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：乘客、司机、一次叫车请求，以及一趟行程——它的生命周期是一张**显式的
  状态机**：REQUESTED → MATCHED → ARRIVED → IN_PROGRESS → COMPLETED，CANCELLED 只能从前三个
  状态到达。非法转移抛异常，每次转移留痕。动手前先决定一件事：**取消权限**该不该和转移表放在
  一起？（想想「还没人接单的行程，司机能不能取消」。）
- 第 2 关（约 15 分钟）：匹配成为一条缝。默认最近优先，但要能换成「距离 + 评分 + 空闲时长」的
  打分。**真正的重点不是打分函数**，而是派单流程：一次只把要约（offer）发给**一位**司机、带
  超时、司机可以拒；要约敞开期间这位司机必须被**独占**，否则两位乘客会匹配到同一辆车；拒单或
  超时要立刻顺位发给下一位，且同一位司机对同一趟行程只问一次。再想一想：所有候选都拒绝了，
  这趟行程停在哪个状态？
- 第 3 关（约 15 分钟）：并发。二十位乘客、八位司机同时下单，用真线程加一个 `threading.Barrier`
  去测，断言的是**不变量**（没有司机同时跑两趟；处在 REQUESTED 的行程必定恰好有一张敞开的
  要约），不是时序。测试里绝不 `sleep`——把时钟注入进去。
- 第 4 关（选做）：计价（起步价 + 里程 + 时长）加一个可插拔的动态加价（surge）策略，说清楚倍数
  在什么时刻锁死；再加拼车——第二位乘客上同一辆车。评分点不是实现，而是**加它们有没有动到状态
  机、要约机制和司机池里的任何一行代码**。

**怎么练**：把 `vault/domains/low-level-design/problems/ride-sharing/starter.py` 的方法体补全，
然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/ride-sharing -q`。

**评分点**
- 司机是被**问**的不是被指派的：产出一张会过期、只发给一位司机的要约，而不是直接把行程写到他身上；说得出广播抢单适用于谁（[[problems-ride-sharing-offer-not-assignment]]）。
- 「被要约占着」是一个**状态**（OFFERED），占用是锁内的一次比较并交换，不是 `is_available` 布尔加先查后写；说得出 GIL 在这里什么都不保证（[[problems-ride-sharing-offered-status-cas]]、[[concurrency-check-then-act]]）。
- 释放与提交只认当前持有者，迟到的超时清扫不会把已经在跑下一单的司机打回空闲（[[problems-ride-sharing-offered-status-cas]]、[[concurrency-lock-while-calling-out]]）。
- 拒单和超时走同一条路径；排除集保证同一位司机不被反复骚扰；候选耗尽时行程拿到一个**终态**而不是永远停在「正在找车」（[[problems-ride-sharing-decline-timeout-and-terminal]]）。
- 状态是枚举加**两张**显式的表（能往哪走 / 谁有权走），既不是布尔汤也不是每状态一个类，并说得出判据（[[problems-ride-sharing-two-tables-not-state-classes]]、[[structure-state-table-vs-state-pattern]]）。
- IN_PROGRESS 只通向 COMPLETED：中途下车是「提前结束并计费」，不是取消（[[problems-ride-sharing-in-progress-is-not-cancellable]]、[[structure-state-guards-and-illegal-events]]）。
- 匹配策略是一个普通函数而不是一族抽象基类；说得出打分的量纲问题，并用 `(score, driver.id)` 打破并列（[[problems-ride-sharing-match-policy-is-a-function]]、[[patterns-command-callable-vs-class]]）。
- 加价倍数在下单那一刻锁死并写进行程，用 `Fraction` 不用 `float`，金额是整数分（[[problems-ride-sharing-surge-locked-at-request]]）。
- 行程从第 1 关起就持有一串「腿」，所以拼车只是追加一条腿、状态轨迹一行不变（[[problems-ride-sharing-legs-make-pooling-free]]、[[patterns-extensibility-followup]]）。
- 内部容器会缩小：要约表在接单／拒单／超时／取消四条路径上都被摘干净，排除集随行程终结而删除。

**题解**：[[solution-ride-sharing]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
