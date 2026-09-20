---
id: problems-rate-limiter-sharded-lock
node: problems.components.rate-limiter
type: qa
step: 7
tags: [grown]
---
## Q
多线程限流器（Rate Limiter）的锁该怎么加？「每个 key 一把锁」为什么是个陷阱？Python 的 GIL 在这里帮得上忙吗？

## A
用**分片锁**（sharded lock）：固定 N 个分片，每片一把 `threading.Lock` 加一个自己的 key→状态 字典，`hash(key) % N` 决定归属。

- **全局一把锁**：正确但所有 key 互相排队，而限流器坐在每个请求的必经之路上。
- **每个 key 一把锁**：粒度最细，但那本「锁的字典」自己也要一把锁保护，而且**它同样会无限增长**——为了解决一个容器的回收问题，造出了第二个更难回收的容器（删一把可能正被持有的锁是经典竞态）。
- **分片**：锁数量是常数，不需要生命周期管理；竞争降到约 1/N；同一个 key 的所有读写天然在同一把锁下；扫描回收时只锁一个分片，其余流量照常通过。

GIL（全局解释器锁）保证单条字节码不被撕开，所以 `dict.get` 不会读到半个对象；它**不**保证 `check` 到 `commit` 之间不切换线程。`used + cost <= capacity` 是一次检查再动作（check-then-act），两百个线程能同时看到「还剩 50 个令牌」然后各自扣一个。锁保护的不是数据结构，是这条复合操作的原子性。
