---
id: problems-reddit-vote-idempotency-natural-key
node: problems.social.reddit
type: qa
step: 5
tags: [grown]
---
## Q
In a voting system, why does making the primary key of the vote table `(userId, targetId, targetType)` itself, storing the current `direction` per row, make votes idempotent without needing a client-supplied idempotency token?

## A
Because the same user voting on the same target twice — whether from a genuine vote change or a network retry of the same request — always resolves to an upsert on the same row, and applying a vote computes a delta relative to whatever direction was previously stored there (e.g. switching from upvote to downvote yields delta ups −1, downs +1). A duplicate request for the same direction produces a delta of zero, so the same vote can never be double-counted; the natural key IS the idempotency key because the system stores current vote state rather than appending a log of vote events.

## Q zh
在一个投票系统里，为什么把投票表的主键直接设成 `(userId, targetId, targetType)`、每行存当前的 `direction`，就能让投票天然幂等，而不需要客户端另外传一个幂等令牌？

## A zh
因为同一个用户对同一个目标的第二次投票——无论是真的改票还是同一请求的网络重试——总是解析成对同一行的一次 upsert，应用一次投票时算出的是相对该行之前存的方向的 delta（例如从赞成改成反对，delta 是赞成 −1、反对 +1）。同一方向的重复请求算出的 delta 是零，所以同一票永远不会被重复计数；这个自然键本身就是幂等键，因为系统存的是当前投票状态，而不是追加一份投票事件日志。
