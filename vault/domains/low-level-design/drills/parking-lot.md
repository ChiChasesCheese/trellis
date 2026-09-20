---
nodes: [problems.machines.parking-lot, patterns.strategy, structure.storage]
tags: [problem]
---
# Drill：停车场（Parking Lot）

一座三层的停车场，车位分摩托车位／小车位／大车位三种，入口和出口各有好几个闸机同时在跑。
照真实机考的节奏分关来做，做完一关再看下一关的要求。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：单层停车场，车辆按尺寸找一个能装下它的空位入场、发一张 Ticket；
  凭 Ticket 出场并释放车位。车位满了、Ticket 无效或已经用过，都要抛出明确的异常，不能让
  调用方自己判断。
- 第 2 关（约 15 分钟）：让车位分配规则可换（至少支持"离入口最近优先"和"把车流分摊到各层"
  两种），让计费规则可换（至少支持按小时计费和一口价，尽量再加一种阶梯计价）——都不能改
  第 1 关写好的 `ParkingLot` 本身。
- 第 3 关（约 15 分钟）：多个入口闸机、多个出口闸机并发操作同一个 `ParkingLot`，绝不能有
  两辆车被分到同一个车位，也不能因为锁的粒度太粗让所有闸机互相卡死。
- 第 4 关（选做）：加一块按楼层显示空闲车位数的展示牌，以及一种新的车辆/车位尺寸（比如
  大巴）——两者都不应该要求你回头改动前三关已经写好、测试通过的类；展示牌也不应该拿到
  `ParkingLot` 内部的车位列表去自己数，只能用它公开暴露的快照/事件接口。

**怎么练**：把 `vault/domains/low-level-design/problems/parking-lot/starter.py` 的方法体补全，
然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/parking-lot -q`。

**评分点**
- 车位的占用状态只放在车位对象自己身上，不额外开一本"占用车位 id 集合"去对齐（[[problems-parking-lot-spot-owns-state]]）。
- 车辆和车位的尺寸用一把可比较的等级表达，靠数值比较判断"装不装得下"，不用继承树和 `isinstance` 判断（[[problems-parking-lot-size-as-ordinal]]）。
- 没有状态的一次性策略（车位分配）写成普通函数，不为它单开一个只有一个方法的抽象基类（[[problems-parking-lot-allocation-function-not-class]]、[[patterns-strategy-callable]]）。
- 只有真的需要暴露不止一个相关方法（比如阶梯计价的明细查询）时，策略才升级成类（[[problems-parking-lot-tiered-needs-class]]、[[patterns-strategy-class-when]]）。
- 说得出"停车场只有一个"这条业务事实不等于要把 `ParkingLot` 做成 Singleton，以及为什么不做（[[problems-parking-lot-no-singleton]]、[[patterns-singleton-costs]]）。
- 并发场景下能说清楚锁保护的到底是哪几行、GIL 为什么不能替代这把锁（[[problems-parking-lot-lock-scope]]）。
- 能现场演示"新增展示牌不改 `ParkingLot`"，说出这依赖的是提前留好的订阅挂钩（[[problems-parking-lot-display-board-zero-touch]]）。
- 对外只暴露一份不可变的空闲数快照（`free_counts_by_floor()`）和自描述的车位事件，从不把内部的车位列表或字典直接返回给调用方（[[structure-api-leaking-internals]]）。
- 计费函数对不足一小时的停留正确向上取整、有最低计费时长，而不是让隐藏测试卡在这个边界上（[[problems-parking-lot-ceiling-hours-mistake]]）。
- 能用[[patterns.strategy|策略模式与可替换算法（Strategy）]]的语言解释"策略模式"在这道题里既有函数形式也有类形式，两者的取舍标准是什么（[[patterns-strategy-parking-lot]]）。

**题解**：[[solution-parking-lot]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
