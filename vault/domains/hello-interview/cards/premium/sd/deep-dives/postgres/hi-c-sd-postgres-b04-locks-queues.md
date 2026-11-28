---
id: hi-c-sd-postgres-b04-locks-queues
node: sd.deep-dives.postgres.beyond
type: qa
step: 4
---
## Q
**PostgreSQL · 行锁的进阶用法：死锁与 SKIP LOCKED**｜拓展 · 加分

多个事务锁多行时怎么死锁？怎样用数据库实现一个任务队列？

## A
- **死锁：** 事务 1 先锁 A 再锁 B，事务 2 先锁 B 再锁 A，互相等待。PostgreSQL 会检测到并中止其中一个（默认等待约 1 秒后检查），应用要能重试。预防办法是让所有事务按相同顺序加锁，例如按主键排序。
- **`NOWAIT`：** 拿不到锁就立刻报错，避免排队。
- **`SKIP LOCKED`：** 跳过已被别人锁住的行，不等待。
- **任务队列：** 每个工作进程在事务内执行 `SELECT ... WHERE status='pending' ORDER BY id LIMIT 1 FOR UPDATE SKIP LOCKED`，取到一个没人处理的任务，处理完更新状态后提交。多个工作进程不会抢同一行，也不互相阻塞。
- **边界：** 中等吞吐的队列用它足够，省掉独立的消息队列；吞吐很高或要扇出多个消费者时仍应使用 Kafka 等专用系统。
