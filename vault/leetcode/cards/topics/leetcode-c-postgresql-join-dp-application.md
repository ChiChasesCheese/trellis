---
id: leetcode-c-postgresql-join-dp-application
node: topics.uncategorised
type: qa
anki: 1787361365497
tags: [algorithm::cost-based-optimization, algorithm::dynamic-programming, algorithm::subset-enumeration, application, case, case::postgresql-join-dp, category::storage-databases, chapter::07, leetcode, system::postgresql]
---
## Q
PostgreSQL join-order DP 的状态和转移分别是什么？为什么 join 多时要切 GEQO？

## A
状态是已连接 relation 的 subset 及候选 paths；转移把两个可连接子集组合并比较估算 cost。subset 数指数增长，join 多时 GEQO 用启发式搜索限制 planning latency。

**Evidence**

PostgreSQL 官方 planner 文档与 joinrels.c 展示按 join level 构造 join relations，并在大 join 集合上使用 GEQO。

[原文 ↗](obsidian://open?vault=lc&file=cases%2Fstorage-databases%2FPostgreSQL%20Join%20Planner%EF%BC%9A%E5%AD%90%E9%9B%86%E5%8A%A8%E6%80%81%E8%A7%84%E5%88%92%E4%B8%8E%20GEQO%20%E8%BE%B9%E7%95%8C)
