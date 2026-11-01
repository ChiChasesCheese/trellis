---
id: hi-sd-cassandra-8-ticketmaster-case
node: qb.sd.notification-system-scale.pre-sd-deep-dives-cassandra
type: qa
step: 8
---
## Q
**案例：Ticketmaster 浏览页的分区与反规范化**｜系统设计 · 深入专题

用 Cassandra 支撑购票浏览页（看场馆座位可用情况）时，表怎么设计？为什么按 section 分区，还要加一张汇总表？

## A
**要点。** 浏览页不要求强一致：选座进入结算时再去强一致库确认。

初版 `PRIMARY KEY (event_id, seat_id)`：一个活动一个分区，万级座位的活动要现场汇总总数与价格，热门活动会被反复算。

改进：按场馆分区查看的体验，把 `section_id` 加进分区键：`PRIMARY KEY ((event_id, section_id), seat_id)`。每个区一个分区，活动分散在多个节点，分区更小，也正好对应「点进某区看座位」。

再建汇总表 `event_sections (event_id, section_id, num_tickets, price_floor)`，分区键 `event_id`。区的数量通常不到 100，单分区就能读完，用预先算好的区余票、起步价展示整张场馆图。

**为什么。** 这就是反规范化：与其让库现场聚合或跨分区查询，不如提前存好。

**取舍。** 汇总数不必精确（页面也只显示「100+」），可容忍最终一致。
