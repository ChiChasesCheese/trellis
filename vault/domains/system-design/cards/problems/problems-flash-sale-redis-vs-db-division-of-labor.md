---
id: problems-flash-sale-redis-vs-db-division-of-labor
node: problems.commerce.flash-sale
type: qa
step: 5
tags: [grown]
---
## Q
A flash sale system uses a Redis Lua script as the primary atomic gate for inventory, then synchronously writes a durable reservation record to a relational database immediately after a successful decrement. Why not just do the atomic conditional decrement directly against the relational database, the way a ticket-booking or hotel-reservation system does for its inventory?

## A
A relational database's single-row conditional UPDATE has a much lower realistic throughput ceiling (an assumed few thousand rows/sec for a single primary) than an in-memory Redis instance (roughly 180,000 ops/sec unpipelined per Redis's own benchmark), and the unthrottled naive peak in a flash sale (100,000/sec) is close enough to that database ceiling to be unsafe without admission control doing essentially all the work first. Redis handles the first, highest-throughput gate (is any stock left), and the database — whose write volume has already been shaped down by admission control to a few thousand/sec — handles durable, auditable record-keeping; the two aren't interchangeable, they're solving different problems at different points in the funnel.

## Q zh
秒杀系统用 Redis Lua 脚本作为库存的主要原子准入关卡，扣减成功后立刻同步把一条持久化的预留记录写入关系型数据库。为什么不像票务预订或酒店预订系统那样，直接对关系型数据库做原子条件扣减？

## A zh
关系型数据库单行条件更新的现实吞吐上限（假设单主库只有几千行/秒）远低于内存中的 Redis 实例（按 Redis 官方基准约 18 万次操作/秒，不开 pipelining），而秒杀未经限流的裸峰值（10 万/秒）已经逼近这个数据库上限，如果没有准入控制先把大部分工作做完，直接打数据库并不安全。Redis 负责第一道、吞吐要求最高的关卡（还有没有库存），而数据库——此时的写入量已经被准入控制削减到几千/秒——负责持久化、可审计的记录留存；两者不是互相替代的关系，而是在漏斗的不同位置解决不同问题。
