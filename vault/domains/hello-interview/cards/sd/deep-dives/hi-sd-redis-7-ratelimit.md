---
id: hi-sd-redis-7-ratelimit
node: qb.sd.messenger-chat-system.pre-sd-deep-dives-redis
type: qa
step: 7
---
## Q
**用 Redis 做限流**｜系统设计 · 深入技术

用 Redis 怎样实现固定窗口限流和滑动窗口限流？有哪些容易漏掉的细节？

## A
**要点。**
- 固定窗口：每个请求对当前窗口的计数键做 `INCR`，超过 N 就拒绝（常用 429 并带 `Retry-After`），否则放行。
- 滑动窗口：每个用户一个有序集合，分数是请求时间戳。每个请求依次：`ZREMRANGEBYSCORE` 删掉窗口外的记录，`ZCARD` 数剩余数量，不足 N 则 `ZADD` 新请求。

**易错。** 只在 `INCR` 返回 1（窗口内第一个请求）时才设置过期时间；如果每个请求都调用 `EXPIRE`，持续有流量时窗口永远不会重置。而且 `INCR` 与 `EXPIRE` 应放在同一个 Lua 脚本里，否则两条命令之间崩溃会留下一个永不重置的计数器。滑动窗口的几步也要放进 Lua 脚本保证原子。

**使用时机。** 被问到分布式限流时，说「Redis 计数器加 Lua 脚本」即可，再根据精度需求选固定或滑动窗口。
