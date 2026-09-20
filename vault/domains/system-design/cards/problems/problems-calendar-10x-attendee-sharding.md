---
id: problems-calendar-10x-attendee-sharding
node: problems.realtime.calendar
type: qa
step: 8
tags: [grown]
---
## Q
In a calendar design, daily active users grow 10x (from 60 million to 600 million) with the same behavior mix. RSVP-write peak QPS grows proportionally from about 2,083 to about 20,833. Given a single relational primary's assumed ceiling of about 3,000 conditional updates/sec, what happens to the safety margin, and what design change does this force?

## A
The safety margin collapses from about 1.44x (3,000 / 2,083) to about 0.14x (3,000 / 20,833) — a single relational primary can now sustain barely a seventh of the required peak, not just an uncomfortably thin margin but an outright shortfall. This forces the Attendee table to be sharded (e.g. by hashed event id) across multiple independent relational clusters, each handling a fraction of the write load and each retaining its own margin, the same direction the per-user free/busy range index must also shard in at this scale so a single free/busy query only touches the shard(s) holding its own attendees' data.

## Q zh
在日历设计里，日活用户增长 10 倍（从 6000 万到 6 亿），行为比例不变。RSVP 写入峰值 QPS 相应从约 2,083 增长到约 20,833。已知单个关系型主库假设的上限约为 3,000 次条件更新/秒，安全边际会怎样变化？这会迫使设计做出什么改变？

## A zh
安全边际从约 1.44 倍（3,000 / 2,083）崩溃到约 0.14 倍（3,000 / 20,833）——此时单个关系型主库连所需峰值的七分之一都撑不住，已经不只是边际薄，而是彻底的容量缺口。这迫使 Attendee 表必须（比如按哈希后的事件 id）分片到多个独立的关系型集群上，每个集群各自承担一部分写入负载、各自保留自己的边际，这和这个规模下每用户 free/busy 范围索引也必须分片的方向一致，让单次 free/busy 查询只命中持有该用户参会人数据的那个分片。
