---
id: problems-typeahead-trending-booster-patch-layer
node: problems.search.typeahead
type: qa
step: 5
tags: [grown]
---
## Q
A daily batch aggregation job produces the base prefix-to-top-K ranking for a typeahead system, but a query that starts trending right after that day's batch run would not appear in suggestions for up to a full day under batch alone. What layer fixes this, and why does it apply a patch rather than replace the whole cache?

## A
A separate streaming layer (a trending booster) computes an approximate count over a short recent window (e.g. the last hour) and identifies which queries are surging well above their historical batch baseline. It emits a small incremental patch — just the handful of surging prefixes and their boosted candidates — merged into the existing precomputed cache, rather than recomputing or replacing the entire prefix structure. This keeps the cost of reacting to a sudden trend proportional to the small number of prefixes actually affected, instead of paying the cost of a full batch rerun every time freshness needs to improve.

## Q zh
一个每日批处理任务产出 typeahead 系统里'前缀到 top-K'的基础排名，但一个恰好在当天批处理跑完之后才开始流行的查询词，单靠批处理最多要等将近一整天才会出现在建议里。什么层解决了这个问题？为什么它是打补丁而不是替换整个缓存？

## A zh
一个独立的流式层（趋势助推器/trending booster）在一个较短的最近窗口（比如最近 1 小时）内做近似计数，识别出哪些查询词的热度明显超出了它们的历史批处理基线。它产出一个小的增量补丁——只包含这一小撮正在飙升的前缀及其提权后的候选——合并进已有的预计算缓存，而不是重新计算或替换整个前缀结构。这样响应突发趋势的成本和实际受影响的前缀数量成正比，而不是每次需要提升新鲜度就要付出一次完整批处理重跑的代价。
