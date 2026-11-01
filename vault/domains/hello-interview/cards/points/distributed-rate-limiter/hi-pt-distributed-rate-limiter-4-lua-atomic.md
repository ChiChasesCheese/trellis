---
id: hi-pt-distributed-rate-limiter-4-lua-atomic
node: qb.sd.distributed-rate-limiter.points
type: qa
step: 4
---
## Q
**分布式限流器 · 原子性与 Lua**｜出自：分布式限流器 › 深入 1

令牌桶要在 Redis 里完成读状态、补令牌、判定、写回。两个网关同时检查同一客户端会出什么问题？怎么解决？

## A
**问题。** 两个网关各读到旧值，双双放行。
**做法。** 用 Redis Lua 脚本在服务端一次执行，读改写原子，也只占一次网络往返。
**细节。** 时间用 Redis 的 TIME 而不是网关本地时间，避免多网关时钟偏差；设置 PEXPIRE，让不活跃客户端的桶自动消失。
