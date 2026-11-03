---
id: hi-pt-rate-limiter-system-6-per-key-lock
node: qb.lld.rate-limiter-system.points
type: qa
step: 6
---
## Q
**限流器（单机类设计） · 并发：per-key 锁**｜必会 · 出自：限流器（单机类设计） › 深入 1

多线程对同一个 key 并发调用会超限，怎么办？全局锁、per-key 锁、无锁怎么选？

## A
**问题。** 先读计数再写回，各读到旧值，双双放行。
**选用。** per-key 锁，让读状态、判定、写状态成为一个临界区。
**对比。** 全局锁所有 key 串行；无锁 CAS 要把多个字段打包成不可变对象再整体 CAS，复杂。
**死锁。** 不同时持有全局锁和 key 锁：全局锁只保护创建条目，释放后再取 key 锁。
