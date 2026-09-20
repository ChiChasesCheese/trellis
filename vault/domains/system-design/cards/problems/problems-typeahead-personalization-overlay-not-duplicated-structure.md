---
id: problems-typeahead-personalization-overlay-not-duplicated-structure
node: problems.search.typeahead
type: qa
step: 6
tags: [grown]
---
## Q
In a typeahead design with 300M DAU, storing even a small per-user recent-history list (about 20 recent queries, ~2KB per user) for every active user costs about 600GB total, roughly 50x more than the entire global precomputed prefix structure (~12GB). Given this, how should personalization be implemented?

## A
Personalization should not maintain a full duplicated candidate structure per user — that would cost far more than the shared global structure it's meant to complement. Instead, keep only a small per-user recent-history list, and apply personalization as a lightweight request-time rerank: fetch the global top-K candidates for the prefix from the shared cache, then boost or reorder that small candidate set using the requesting user's own recent history, rather than computing or storing personalized candidates ahead of time for every user.

## Q zh
在一个服务 3 亿日活的 typeahead 设计中，即使只为每个活跃用户保存一份很小的最近查询历史列表（约 20 条最近查询，每用户约 2KB），总存储成本也约为 600GB——大约是整个全局预计算前缀结构（约 12GB）的 50 倍。据此，个性化应该怎么实现？

## A zh
个性化不应该为每个用户维护一整套复制出来的候选结构——那样的代价会远超它本该辅助的共享全局结构本身。正确做法是只保留一份很小的每用户最近历史列表，把个性化实现成一次请求时的轻量重排：先从共享缓存里取出该前缀的全局 top-K 候选，再用发起请求的用户自己的最近历史对这个小候选集做提权或重排，而不是为每个用户提前计算或存储一整套个性化候选。
