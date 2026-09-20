---
id: problems-digital-wallet-deterministic-reducer
node: problems.commerce.digital-wallet
type: qa
step: 5
tags: [grown]
---
## Q
In a digital wallet built with event sourcing, why must the function that replays a wallet's event log into a balance be a pure, deterministic function with no external dependencies?

## A
If the replay function reads any external or mutable state (the current wall-clock time, a live exchange-rate lookup, a random number), replaying the exact same event sequence twice can produce two different balances — and this divergence is invisible during normal operation, since a wallet is usually replayed only once, surfacing only when a shard is rebuilt from its log after a crash or migrated to a new shard. Determinism (balance = pure_reduce(events), depending only on the event sequence itself) is what makes crash recovery and shard migration safe: replaying the same log anywhere must always reconstruct the identical balance, verifiable by checking the replayed result is byte-identical on the source and target shard.

## Q zh
在一个用事件溯源构建的数字钱包中，为什么把事件日志重放成余额的函数必须是一个不依赖任何外部状态的确定性纯函数？

## A zh
如果重放函数读取任何外部或可变状态（当前的挂钟时间、实时汇率查询、随机数），重放同一段事件序列两次可能得到两个不同的余额——而这种分歧在正常运行时是不可见的，因为一个钱包通常只被重放一次，只有在分片崩溃后从日志重建、或账户被迁移到新分片时才会暴露。确定性（余额 = pure_reduce(events)，只依赖事件序列本身）正是崩溃恢复和分片迁移得以安全进行的前提：在任何地方重放同一段日志都必须重建出完全相同的余额，可以通过校验源分片和目标分片重放结果逐字节相等来验证。
