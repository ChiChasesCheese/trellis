---
nodes: [amazon.amz-parking-fees, patterns.strategy, problems.machines.parking-lot]
tags: [problem]
---
# Drill：停车场计费（Parking Lot Fees）

车进场领票，出场凭票结算：系统按停车时长、车型和时段算出该付多少钱。车位分配在题库的停车场里已经做过，这里只做出场那一笔账。
每一关都在检验同一件事：新的计价场景是落在价目表和一个新类上，还是迫使你改已写好的核心方法。
（报告只说「重点在计费、不同场景有不同逻辑」，具体费率和第 3、4 关均为推断。）

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 15 分钟）：按车型的小时单价，`enter(plate, vehicle)` 发票，`exit(ticket_id)` 算钱并作废票。想清楚金额类型、不足一小时怎么收、重复使用同一张票怎么办。
- 第 2 关（约 15 分钟）：工作日 08:00–20:00 是高峰，夜间和周末是非高峰；一次停留可能跨过这些边界。手算一个周五 19:30 入场、周六 08:30 出场的例子再写代码。
- 第 3 关（约 10 分钟）：前 15 分钟免费；每车型每个日历日封顶。
- 第 4 关（选做）：会员折扣与丢票罚款（注意两者的顺序）；两个出口同时扫同一张票。

**怎么练**：把 `vault/domains/low-level-design/problems/amz-parking-fees/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/amz-parking-fees -q`。

**评分点**
- 开场问了取整与宽限期、费率随什么变、封顶口径与丢票（[[amz-parking-fees-how-asked-and-three-questions]]）。
- 对象职责清楚：价目表、引擎、调整、票各有变化原因（[[amz-parking-fees-objects-and-their-jobs]]）。
- 第 1 关沿变价时刻切段，金额是整数分，每天取整一次（[[amz-parking-fees-stage1-bill-by-segments]]）。
- 跨边界的停留算对，能手算出 2700 分（[[amz-parking-fees-stay-crossing-rate-boundary]]）。
- 场景做成数据而不是 if 链或每场景一个类（[[amz-parking-fees-tariff-data-vs-scenario-classes]]）。
- 封顶按日历日，放在价目表里（[[amz-parking-fees-followup-daily-cap-per-calendar-day]]）。
- 调整有显式顺序，丢票用车牌找回入场记录（[[amz-parking-fees-lost-ticket-adjustment-order]]）。
- 取票在锁内一次完成，计价在锁外（[[amz-parking-fees-concurrency-two-exits-one-ticket]]）。
- 不对每段单独取整（[[amz-parking-fees-common-mistake-rounding-per-segment]]）。

**题解**：[[solution-amz-parking-fees]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
