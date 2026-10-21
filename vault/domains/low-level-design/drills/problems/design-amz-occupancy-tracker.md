---
nodes: [amazon.amz-occupancy-tracker, structure.storage]
tags: [problem]
---
# Drill：办公室人数追踪（Occupancy Tracker）

员工刷卡进出办公室，系统要回答「现在多少人」「过去某一时刻多少人」「某段时间内最多有过多少人」。
规模从几十人到几千人，事件按时间追加。每一关检验的是：数据模型选对了，后面的需求是不是只多一个方法或一个类。第 4 关选做。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：记录进入和离开，回答当前人数。想清楚：存什么？没进就出、进了又进怎么处理？
- 第 2 关（约 15 分钟）：回答任意时间戳的人数，再回答区间 [a, b] 内出现过的最大人数。时间戳等于事件时间算不算？区间开始时已在楼里的人呢？
- 第 3 关（约 15 分钟）：有多个楼层；刷卡机会重发事件，事件也可能晚到。各自怎么处理？
- 第 4 关（选做）：同一个模型写成 SQL；查询很多时怎么加速；多个闸机并发上报。

**怎么练**：把 `vault/domains/low-level-design/problems/amz-occupancy-tracker/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/amz-occupancy-tracker -q`。

**评分点**
- 开场问了历史还是现在、事件顺序、区域数（[[amz-occupancy-tracker-how-asked-and-three-questions]]）。
- 对象职责清楚：事件、时间线、校验入口（[[amz-occupancy-tracker-objects-and-their-jobs]]）。
- 第 1 关先校验再写入，失败不留脏数据（[[amz-occupancy-tracker-stage1-enter-leave-in-code]]）。
- 前缀和加 `bisect_right`，查询 O(log n)，边界正确（[[amz-occupancy-tracker-count-at-prefix-sum-and-bisect]]）。
- `max_in` 算上区间开始时的人数，说得出线段树的取舍（[[amz-occupancy-tracker-decision-range-max-start-count-and-segment-tree]]）。
- 区域各一条时间线，知道峰值不能相加（[[amz-occupancy-tracker-followup-zones-peaks-do-not-add]]）。
- 区分重试与非法序列，迟到事件有明确策略（[[amz-occupancy-tracker-failure-path-duplicate-and-late-events]]）。
- 能写出 SQL 版，并说出加速办法（[[amz-occupancy-tracker-sql-version-and-scale]]）。
- 校验与追加在同一把锁里（[[amz-occupancy-tracker-concurrency-validate-and-append-under-one-lock]]）。

**题解**：[[solution-amz-occupancy-tracker]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
