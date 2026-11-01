---
id: hi-sd-ticketmaster-6-reserve-redis
node: sd.problem-breakdowns.ticketmaster
type: qa
step: 6
---
## Q
**分布式锁加 TTL（Redis）**｜系统设计 · 问题拆解

为什么已经有 PostgreSQL 还要用 Redis 做座位预订的锁？它怎么工作，多座位怎么加锁？

## A
**为什么。** 需要自动过期的临时预订，而 PostgreSQL 没有原生的行级 TTL，要靠应用层 cron；Redis 自带键过期，且在内存里，加锁解锁极快。

**做法。** 选座时以 ticketId 为键、userId 为值，用 `SET key value NX EX seconds` 原子加锁，同一时刻只有一个客户端成功。付款完成，数据库把票改为 booked，应用主动删锁；超时则 Redis 自动释放。票表只剩 available 和 booked 两态，预留完全由 Redis 管。值存用户 ID，确认时可验证是同一个人。

**多座位。** 依次逐张加锁，任何一张失败就释放已拿到的；若这些票落在同一 Redis 节点，可用 Lua 脚本一次原子加锁。

**兜底。** 数据库仍用 OCC 或行锁，保证锁失效时也不会双订。
