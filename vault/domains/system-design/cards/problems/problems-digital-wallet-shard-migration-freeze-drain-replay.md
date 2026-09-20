---
id: problems-digital-wallet-shard-migration-freeze-drain-replay
node: problems.commerce.digital-wallet
type: qa
step: 7
tags: [grown]
---
## Q
In an event-sourced digital wallet, how is a single account migrated from one shard to another without risking its balance diverging between the source and target?

## A
The account is frozen first (new transfer prepares against it are rejected, other accounts are unaffected), then drained by waiting for every in-flight transfer already prepared against it to reach a terminal state (committed or cancelled) — bounded because the transfer coordinator tracks an explicit terminal status per transfer rather than waiting indefinitely. Its full event history is then copied to the target shard and replayed there with the same deterministic reducer used everywhere else; migration is only accepted once the replayed balance on the target is byte-identical to the source. Only then does routing cut over atomically and the account unfreeze — the only unavailability window is the drain step, not the whole copy.

## Q zh
在一个事件溯源的数字钱包中，如何把单个账户从一个分片迁移到另一个分片，同时避免它的余额在源分片和目标分片之间产生分歧？

## A zh
先冻结该账户（拒绝针对它的新转账 prepare 请求，不影响其他账户），然后排空——等待所有已经针对它 prepare 的在途转账都到达终态（committed 或 cancelled），这个等待是有界的，因为协调者对每笔转账都记录了明确的终态，而不是无限期等待。接着把它完整的事件历史复制到目标分片，用和其他所有地方相同的确定性 reducer 在目标分片上重放；只有当目标分片重放出的余额与源分片逐字节相等时，迁移才被接受。之后才原子地切换路由并解冻账户——唯一的不可用窗口是排空这一步，而不是整个复制过程。
