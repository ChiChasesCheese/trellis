---
nodes: [problems.booking.meeting-scheduler, structure.storage]
tags: [problem]
---
# Drill：会议室预订（Meeting Scheduler）

一家几千人的公司：几十间会议室分布在不同楼层，员工分布在不同城市甚至不同时区，站会、评审这类
会议大多每周重复。像真实的机器编码轮一样分关来做，做完一关再看下一关。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：先想清楚一段占用的时间边界怎么定——`10:00–11:00` 的会和紧接着开始的
  `11:00–12:00` 算不算冲突，准备好向面试官讲清楚你的选择为什么不需要额外的特判。建出房间（容量、
  设备）、订一段会议、冲突时拒绝。
- 第 2 关（约 15 分钟）：给一组与会人找一个大家都有空、时长够、还配得到房的时间段。先想清楚
  "多个人的忙碌区间怎么合并"，讲得出朴素的两两比较和你选的算法复杂度差在哪里；配房要选坐得下
  这组人的最小那间。
- 第 3 关（约 15 分钟）：加周期会议——每周重复，可能隔周。想清楚"规则"和"例外"该怎么分开存，
  规则要不要在创建时就把未来所有场次都算出来。再加两种编辑："只改这一次"和"这一次及以后全改"，
  说得出这两种编辑分别落在哪个对象上。
- 第 4 关（选做）：加时区——参会人不在同一个城市，一条"每周一 9 点"的规则存的到底是哪个 9 点，
  跨夏令时切换会不会出问题？用真线程测两个组织者同时抢同一间房的重叠时段。

**怎么练**：把 `vault/domains/low-level-design/problems/meeting-scheduler/starter.py` 的方法体
补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/meeting-scheduler -q`。

**评分点**
- 半开区间的选择，讲得出为什么相邻会议天然不冲突、不需要额外特判
  （[[problems-meeting-scheduler-half-open-interval]]）。
- 找空档用区间合并算法而不是两两比较，说得出复杂度差在哪
  （[[problems-meeting-scheduler-merge-intervals-cost]]）。
- 能说清"忙闲"状态为什么该长在房间的日历对象上，而不是房间本身
  （[[problems-meeting-scheduler-room-vs-calendar]]）。
- 周期会议只在查询窗口里按需展开，从不提前把未来场次物化成一张表
  （[[problems-meeting-scheduler-lazy-recurrence-expansion]]）。
- "只改这一次"和"这一次及以后"是两种不同粒度的编辑，说得出后者为什么要新开一条系列而不是改一个字段
  （[[problems-meeting-scheduler-this-vs-this-and-following]]）。
- 周期会议存本地时间加时区，讲得出为什么固定 UTC 瞬间跨夏令时会让本地钟点漂移
  （[[problems-meeting-scheduler-local-time-plus-zone]]）。
- 多把锁固定的嵌套顺序，说得出为什么不会死锁（[[problems-meeting-scheduler-lock-nesting-order]]）。
- 说得出配房逻辑为什么不需要建一个策略模式的类族
  （[[problems-meeting-scheduler-no-strategy-class-for-room-pick]]）。

**题解**：[[solution-meeting-scheduler]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
