---
id: hi-sd-distributed-rate-limiter-5-token-bucket-redis
node: sd.problem-breakdowns.distributed-rate-limiter
type: qa
step: 5
---
## Q
**令牌桶放进 Redis：为什么需要 Lua 脚本**｜系统设计 · 问题拆解

令牌桶的状态怎么跨多个网关共享？流程是什么？为什么 MULTI/EXEC 仍有竞态，怎么修？

## A
**为什么要共享。** 状态在每个网关本地内存里，又回到进程内的老问题：Alice 的 50 次打到 A、50 次打到 B，各自都以为没超。所以用 Redis 作为所有网关共用的事实来源。

**流程。** 网关用 `HMGET alice:bucket tokens last_refill` 读状态，按流逝时间算新增令牌（不超过容量），再写回令牌数与时间戳，并设 `EXPIRE` 1 小时清理闲置桶，令牌够就放行并减 1。

**竞态。** 即便用了 MULTI/EXEC，读（HMGET）在事务之外：两个请求同时读到同样的令牌数，都判断可放行，只剩 1 个令牌却放了 2 个。

**修复。** 把读、算、写整个读改写序列放进一个 Lua 脚本，在 Redis 里原子执行。这是争用（contention）模式的典型：扩大原子边界。

**优点。** 亚毫秒、自动过期、可复制高可用。
