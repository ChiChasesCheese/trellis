---
nodes: [amazon.amz-train-fare, oop.values, patterns.strategy]
tags: [problem]
---
# Drill：火车线路票价（Train Fare Calculator）

一条线性的火车线路上有一串车站，乘客从任意一站上车、任意一站下车，票价按经过的区间数计算；线路会在运行时加站，周末票价要有上限。
规模很小，但每一关都在检验同一件事：新需求是落在一个新类上，还是迫使你改已写好的核心方法。
第 4 关是自然的延伸，选做。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：线路 G→U→H→K→I，相邻站费用 1，实现 `calculate_fare(start, stop)`（G 到 I 是 4）。想清楚方向、同站、未知车站，以及金额用什么类型。
- 第 2 关（约 15 分钟）：线路数据从哪来？设计一个类，支持动态加站；再回答：追加和在中间插入的复杂度各是多少，价格怎么保持正确。
- 第 3 关（约 15 分钟）：周末总票价封顶。先问封的是什么，再写；时间不能在计费逻辑里读系统时钟。
- 第 4 关（选做）：同一乘客同一天累计封顶；工作日高峰加价；多线程同时记账不超封顶。

**怎么练**：把 `vault/domains/low-level-design/problems/amz-train-fare/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/amz-train-fare -q`。

**评分点**
- 开场问了封顶对象、加站方式、区间是否同价（[[amz-train-fare-how-asked-and-three-questions]]）。
- 对象职责清楚，线路、规则、记账各有变化原因（[[amz-train-fare-objects-and-their-jobs]]）。
- 第 1 关代码简洁，处理方向、同站与未知车站（[[amz-train-fare-stage1-calculate-fare-in-code]]）。
- 用前缀和做到 O(1) 查价，说得出追加与中间插入的代价差异（[[amz-train-fare-prefix-sums-and-middle-insertion]]）。
- 封顶做成规则对象而不是核心方法里的 if（[[amz-train-fare-rule-object-vs-if-in-method]]）。
- 时钟注入，新需求只新增一个类（[[amz-train-fare-followup-weekend-cap-and-injected-clock]]）。
- 区分单程封顶与每日累计封顶，并清理旧日期（[[amz-train-fare-edge-per-trip-vs-per-day-cap]]）。
- 读—算—写在一把锁里（[[amz-train-fare-concurrency-lock-read-compute-write]]）。
- 金额用整数分，不用 float，不在逻辑里取现在时间（[[amz-train-fare-common-mistake-now-and-float]]）。

**题解**：[[solution-amz-train-fare]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
