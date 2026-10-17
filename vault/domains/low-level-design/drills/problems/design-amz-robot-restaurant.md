---
nodes: [amazon.amz-robot-restaurant, patterns.state, patterns.strategy]
tags: [problem]
---
# Drill：机器人餐厅（Robot Restaurant）

餐厅里有几台机器人：顾客点单，空闲的机器人接单、做菜、送到桌子，然后回到空闲；机器人有电量，低了要去充电桩。规模很小，但每一关都在检验同一件事：新需求落在哪个类上，状态机的规则放在哪里。
（报告里只有题名；以下各关全部是重建，第 3 关的充电问法借自另一团队的报告。）

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：一台机器人，`place_order(table, dish)` → 做菜 → 送餐 → 回到空闲。时间用离散的 `tick()` 推进，不用 `sleep`。订单有状态，未知菜品要报错。
- 第 2 关（约 15 分钟）：多台机器人，订单先来先服务排队；「哪台接」做成可替换的规则（先写「编号最小」，再写「电量最多」）；能取消还在排队的订单。
- 第 3 关（约 15 分钟）：电量。做菜和送餐耗电；电量低于阈值的空闲机器人去充电，充电桩数量有限；没有空桩、电量又低的机器人怎么办？机器人状态的合法转移要有一张表。
- 第 4 关（选做）：多线程同时下单，每张单恰好送达一次；对外只给只读快照。

**怎么练**：把 `vault/domains/low-level-design/problems/amz-robot-restaurant/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/amz-robot-restaurant -q`。

**评分点**
- 开场问了一条龙还是分工、时间怎么走、分配与电量规则（[[amz-robot-restaurant-how-asked-and-three-questions]]）。
- 订单、机器人、策略、餐厅各有一个变化原因（[[amz-robot-restaurant-objects-and-their-jobs]]）。
- 第 1 关用离散时间推进，没有睡眠（[[amz-robot-restaurant-stage1-tick-flow-in-code]]）。
- 状态机用枚举加合法转移表，非法转移抛异常（[[amz-robot-restaurant-robot-state-machine-transition-table]]）。
- 分配规则是一个拿快照的函数（[[amz-robot-restaurant-assignment-policy-function-vs-class]]）。
- 能说出分工机器人时哪里改、哪里不动（[[amz-robot-restaurant-followup-split-cook-and-delivery-robots]]）。
- 没有空桩时按「做完后电量」判断接不接单，并有下界保证（[[amz-robot-restaurant-edge-low-battery-no-free-charger]]）。
- 一把锁罩住队列与机器人，对外只给快照（[[amz-robot-restaurant-concurrency-one-lock-around-queue-and-robots]]）。
- 充电桩占用数现数，不另设计数器（[[amz-robot-restaurant-common-mistake-charger-counter-leak]]）。

**题解**：[[solution-amz-robot-restaurant]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
