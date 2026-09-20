---
id: problems-ticket-booking-hold-vs-lock-contention
node: problems.commerce.ticket-booking
type: qa
step: 1
tags: [grown]
---
## Q
In an assigned-seating ticket booking system (like Ticketmaster) with 1 million buyers competing for 50,000 seats in the first minute, why is the average 20:1 seat contention ratio not the number that determines the database's write bottleneck?

## A
Because the 1 million requests are spread across 50,000 different rows (seats), so each individual row only sees roughly 20 concurrent conditional-update attempts, not 1 million. The true bottleneck is the database's aggregate row-update throughput across all rows, not lock contention on any single row — a naively-computed 100K QPS peak (1M requests / 10s) overstates per-row contention but understates the total write volume a single relational instance must absorb.

## Q zh
在一个划位（assigned-seating）票务系统（如 Ticketmaster）里，开售第一分钟有 100 万买家争抢 5 万个座位，为什么平均 20:1 的座位竞争比并不是决定数据库写瓶颈的那个数字？

## A zh
因为这 100 万个请求分散在 5 万个不同的行（座位）上，所以单行实际只面对约 20 个并发的条件更新尝试，而不是 100 万个。真正的瓶颈是数据库跨所有行的聚合写吞吐，而不是某一行上的锁竞争——简单算出的 10 万 QPS 峰值（100 万请求 / 10 秒）高估了单行竞争，却低估了单个关系型实例需要承受的总写入量。
