---
id: problems-meeting-scheduler-lazy-recurrence-expansion
node: problems.booking.meeting-scheduler
type: qa
step: 5
tags: [grown]
---
## Q
会议室预订设计里，一条“每周一 9 点、不设结束日期”的周期会议规则，怎么在不提前生成无穷多条记录的前提下回答“三年后某天占不占用”这种查询？

## A
`RecurringSeries` 只存重复规则本身和一张按天记的例外表，从不预先把未来的每一次场次物化成具体的会议记录。展开只发生在查询的那一刻，并且只展开查询窗口覆盖的那几天：把窗口换算成日期范围，按规则筛出落在范围内的具体日期，再逐天换算出那一天的区间。存储量只和“记了多少条例外”有关，和规则已经生效了多久、以后还要跑多久完全无关。
