---
id: problems-ticket-booking-virtual-queue-admission
node: problems.commerce.ticket-booking
type: qa
step: 6
tags: [grown]
---
## Q
In a ticket booking system's virtual waiting room, why does the admission controller throttle to a rate like 3,000-5,000 admits/second based on the downstream seat database's capacity, rather than admitting users as fast as they arrive?

## A
Because entry traffic (up to ~1 million requests/minute for a hot on-sale) can be two orders of magnitude larger than what a single relational seat database can safely absorb as row-update throughput (a few thousand QPS). The admission controller's job is to reshape the traffic spike into a stream the database can sustain, ideally using a feedback signal like database latency or hold-success rate to adjust the admission rate dynamically, rather than admitting on a fixed schedule regardless of downstream load.

## Q zh
在票务系统的虚拟排队厅（虚拟候机厅）里，为什么 admission controller 要按下游座位数据库的承受能力把放行速率限制在每秒 3,000–5,000 人左右，而不是用户到达多快就放行多快？

## A zh
因为一场热门开售的入口流量（峰值可达每分钟约 100 万请求）可能比单个关系型座位数据库能安全承受的行更新吞吐（每秒几千 QPS）高出两个数量级。admission controller 的职责是把这个流量脉冲整形成数据库能持续消化的速率，理想情况下用数据库延迟或占座成功率之类的反馈信号动态调整放行速率，而不是不顾下游负载按固定节奏放人。
