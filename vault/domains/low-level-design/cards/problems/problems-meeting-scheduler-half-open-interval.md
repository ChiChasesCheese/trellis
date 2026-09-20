---
id: problems-meeting-scheduler-half-open-interval
node: problems.booking.meeting-scheduler
type: qa
step: 1
tags: [grown]
---
## Q
在会议室预订（Meeting Scheduler）设计里，为什么用半开区间 `[start, end)` 表示一段会议占用，能让 `10:00–11:00` 和 `11:00–12:00` 天然不算冲突？

## A
半开区间把结束时刻排除在占用之外，重叠判断只需要一行：`self.start < other.end and other.start < self.end`。代入两段相邻的会议，`11:00 < 11:00` 为假，整个表达式为假，不重叠，不需要任何 `-1` 分钟或“端点相等就放行”的特判。如果用闭区间 `[start, end]`，11:00 这一刻会被两段会议同时声明占有，要么误判冲突，要么必须在代码里补一条容易被漏掉的特殊分支。
