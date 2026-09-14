---
id: distributed-materializing-conflicts
node: distributed.transactions.isolation
type: qa
---
## Q
A booking system checks "is room 101 free 12–1pm?" and inserts a reservation — but there is no existing row for the time slot, so `SELECT ... FOR UPDATE` locks nothing and double-bookings slip through. What is the "materializing conflicts" technique, and why is it a last resort?

## A
The failure is a **phantom**: the conflict is between a query predicate and a *future insert*, and you cannot lock rows that don't exist yet.

**Materializing the conflict** manufactures the missing rows: pre-create a table of lockable units — e.g. one row per (room, 15-minute slot) for the next six months, holding no data of interest. Every booking transaction first `SELECT ... FOR UPDATE`s the slot rows it covers; two competing bookings now collide on a concrete row and serialize.

Last resort because:
- It **leaks concurrency control into the data model** — a schema object exists purely to be locked, and every writer must remember the ritual (miss it once, the guarantee is gone).
- The lock-row space must be **enumerable in advance** (time slots work; "usernames anyone might pick" don't — though a unique index covers that case).

Prefer a serializable isolation level (SSI) or index-range locking when the engine offers them; materialize only when they're unavailable or too slow.

## Q zh
一个订房系统先查询"12–1pm 房间 101 空闲吗？"再插入预订记录——但该时间段根本没有已存在的行，`SELECT ... FOR UPDATE` 锁了个寂寞，双重预订照样发生。什么是 materializing conflicts（物化冲突）技术？它为什么只是最后手段？

## A zh
这个失败是一个 **phantom（幻读）**：冲突发生在查询谓词和一个*未来的插入*之间，而你无法锁住尚不存在的行。

**Materializing conflicts** 就是把缺失的行制造出来：预先创建一张"可锁单元"表——例如未来六个月每个（房间，15 分钟时段）一行，本身不承载有意义的数据。每个预订事务先对它覆盖的时段行执行 `SELECT ... FOR UPDATE`；两个竞争的预订现在会在具体的行上碰撞并串行化。

之所以是最后手段：
- 它**把并发控制泄漏进了数据模型**——一个 schema 对象存在的唯一目的就是被锁，而且所有写入方都必须记得这套仪式（漏掉一次，保证就没了）。
- 锁行空间必须**能提前枚举**（时间段可以；"任何人可能取的用户名"不行——不过那种场景 unique index 就能覆盖）。

引擎支持时优先用 serializable 隔离级别（SSI）或 index-range 锁；只有它们不可用或太慢时才物化。
