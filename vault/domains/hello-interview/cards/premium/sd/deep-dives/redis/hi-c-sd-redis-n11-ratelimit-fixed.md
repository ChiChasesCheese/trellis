---
id: hi-c-sd-redis-n11-ratelimit-fixed
node: sd.deep-dives.redis.notes
type: qa
step: 11
---
## Q
**Redis · 限流：固定窗口**｜摘要 · 必会

用 Redis 做固定窗口限流，具体怎么写？为什么只能在第一次请求时设过期？

## A
- **算法：** 保证时间窗口 W 内请求数不超过 N。每来一个请求，对当前窗口的计数键做 `INCR`；超过 N 就拒绝（通常返回 429 和 `Retry-After` 头），否则放行。
- **只在 `INCR` 返回 1 时设 `EXPIRE`：** 如果每个请求都 `EXPIRE`，过期时间被不断往后推，持续有流量的话窗口永远不会重置。
- **INCR 与 EXPIRE 合成 Lua：** 把 `INCR` 和 `EXPIRE` 写成一个 Lua 脚本： 两条命令之间崩溃，会留下一个永不重置的计数器。
- **2026 亮点：** Redis 8.8 起有原生命令 `INCREX`，一条命令原子地加一、封顶、并只在窗口首次设置过期（如 `INCREX key BYINT 1 UBOUND 100 EX 60 ENX`），返回的实际增量为 0 即拒绝，不再需要 Lua。取舍：仍是固定窗口，边界处可能放过两倍突发，要平滑就用滑动窗口或令牌桶；多活（Active-Active）下各副本只按本地值校验上限，合并后可能超限，Redis Cloud 暂不支持。
