---
id: distributed-lost-update-vs-write-skew
node: distributed.transactions.isolation
type: qa
---
## Q
Lost update and write skew are both "two transactions read, then write based on what they read." What structurally separates them, and why do the standard lost-update defenses fail against write skew?

## A
- **Lost update**: both transactions **write the same object** they read (two read-modify-write increments of one counter; one overwrites the other).
- **Write skew**: each transaction **writes a different object** than the other; only the *combination* violates an invariant that spans them (two doctors each removing themselves from the same shift).

Why the defenses don't transfer: lost-update tools all key on a **write-write collision on one object** — atomic operations (`SET n = n + 1`), `SELECT ... FOR UPDATE` on the row being changed, engines that auto-detect concurrent updates to the same row (Postgres repeatable read). In write skew there *is no shared written object* to collide on, so nothing triggers — unless you deliberately lock the rows **read** (the premise), or run truly serializable isolation.

Ordering to remember: dirty write → lost update → write skew is the same race with the shared-object requirement progressively relaxed, and each step evades one more automatic defense.

## Q zh
lost update（丢失更新）和写偏斜（write skew）都是"两个事务先读、再基于读到的内容写"。它们在结构上的区别是什么？为什么针对 lost update 的标准防御对 write skew 无效？

## A zh
- **Lost update**：两个事务**写的是它们读过的同一个对象**（对同一个计数器做两次读-改-写；一个覆盖另一个）。
- **Write skew**：每个事务**写的对象和对方不同**；只有两者的*组合*才违反一个横跨它们的不变量（两位医生各自把自己从同一个班次上撤下）。

防御为何不能迁移：lost update 的工具全都依赖**同一对象上的写-写碰撞**——原子操作（`SET n = n + 1`）、对被修改行的 `SELECT ... FOR UPDATE`、能自动检测同一行并发更新的引擎（Postgres 的 repeatable read）。而 write skew 中*不存在共同写入的对象*可供碰撞，所以什么都不会触发——除非你刻意锁住**读过的**那些行（前提条件），或者使用真正的 serializable 隔离。

记忆顺序：dirty write → lost update → write skew 是同一个竞态，共享对象的要求逐级放松，每放松一级就躲开一种自动防御。
