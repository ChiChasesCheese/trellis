---
id: problems-leaderboard-sorted-set-rebuildable-cache
node: problems.realtime.leaderboard
type: qa
step: 7
tags: [grown]
---
## Q
If a leaderboard's Redis sorted sets are treated as the only place score data lives, what specific recovery capability is lost, and what design keeps that capability while still using Redis's own persistence (RDB/AOF) as a fast-path optimization?

## A
Relying only on Redis's own persistence means recovery can restore whatever was previously written to Redis — including the output of a buggy scoring calculation — but it cannot recompute results under a corrected rule after the fact, since the corrected logic was never applied to the raw inputs. The fix is to treat the sorted sets as a rebuildable cache derived from an authoritative, append-only event log of raw score events (the true source of truth), with Redis's RDB/AOF kept only as a fast-restart optimization on top. This means a scoring bug discovered after the fact can be fixed by replaying the event log with corrected logic to produce a new leaderboard, rather than being permanently baked into whatever Redis happened to have stored.

## Q zh
如果把排行榜的 Redis 有序集合当作分数数据存在的唯一地方，会失去什么具体的恢复能力？什么样的设计能在继续使用 Redis 自身持久化（RDB/AOF）作为快速恢复优化的同时，保留这个能力？

## A zh
只依赖 Redis 自身的持久化，意味着恢复只能还原此前写入 Redis 的内容——包括一次有 bug 的计分逻辑算出的结果——但无法事后用修正过的规则重新计算，因为修正后的逻辑从未被应用到原始输入上过。解决办法是把有序集合当作从一份权威的、只追加的原始分数事件日志（真正的数据来源）派生出的可重建缓存，Redis 的 RDB/AOF 只作为其上的一层快速重启优化保留。这意味着事后发现的计分 bug 可以通过用修正后的逻辑重放事件日志来生成一份新的排行榜来修复，而不是永久固化在 Redis 当时恰好存了什么里。
