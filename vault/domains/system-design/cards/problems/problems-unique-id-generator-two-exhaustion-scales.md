---
id: problems-unique-id-generator-two-exhaustion-scales
node: problems.foundations.unique-id-generator
type: qa
step: 5
tags: [grown]
---
## Q
In a Snowflake-style ID generator, sequence-number exhaustion and worker-id exhaustion are both 'running out of bits,' but why do they require completely different responses?

## A
Sequence exhaustion happens within a single millisecond on a single node when its request rate briefly exceeds the sequence field's per-millisecond capacity (e.g. 1,024 with a 10-bit field); the fix is to spin-wait for the next millisecond tick before continuing, a sub-millisecond stall with no lasting effect, and it must never wrap the counter, which would produce a duplicate of an ID already issued in that same millisecond. Worker-id exhaustion happens at the deployment-topology scale, when the number of active generator instances approaches the worker-id field's total capacity (e.g. 8,192 with 13 bits); once exhausted, new instances simply cannot start (their lease request fails), which is not something a brief wait resolves — it requires reclaiming leases from inactive instances and, eventually, a planned migration to a wider worker-id field with old and new layouts coexisting during a transition period.

## Q zh
在一个 Snowflake 风格的 ID 生成器里，序列号耗尽和 worker id 耗尽都是'位数用完了'，但为什么它们需要完全不同的应对方式？

## A zh
序列号耗尽发生在单个节点的单个毫秒内，当它的请求速率短暂超过序列号字段每毫秒的容量时（例如 10 位字段对应的 1,024 个）；解决办法是自旋等待下一个毫秒 tick 再继续，这只是一次不到 1 毫秒的停顿，没有持久影响，而且绝不能让计数器回绕，回绕会产生和同一毫秒内已发出的 ID 重复的数值。worker id 耗尽发生在部署拓扑的规模级别，当活跃生成实例数量逼近 worker id 字段的总容量时（例如 13 位对应的 8,192 个）；一旦耗尽，新实例根本无法启动（它的租约请求会失败），这不是稍等一下能解决的问题——需要靠回收不活跃实例的租约来缓解，最终还需要一次有计划的迁移，扩大 worker id 字段位宽，迁移期内新旧位布局并存。
