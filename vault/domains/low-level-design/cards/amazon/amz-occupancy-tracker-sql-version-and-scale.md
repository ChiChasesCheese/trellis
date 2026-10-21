---
id: amz-occupancy-tracker-sql-version-and-scale
node: amazon.amz-occupancy-tracker
type: qa
step: 8
tags: [grown]
---
## Q
在办公室人数追踪里，同一个模型怎样写成 SQL？查询很多时怎么加速？

## A
事件表 `presence_events(seq, ts, person, zone, delta)`，`seq` 自增，给同一秒的事件定序。某时刻人数：`SELECT COALESCE(SUM(delta),0) ... WHERE ts <= :t`。区间最大：窗口函数 `SUM(delta) OVER (ORDER BY ts, seq)` 求前缀和，在区间内取 `MAX`，再并上区间开始时的人数。窗口函数每次查询 O(n)，所以写入时物化前缀和，或每分钟存一行（期末人数、该分钟峰值），区间最大只读区间内的分钟行。一天 1 亿事件约每秒 1157 个。
