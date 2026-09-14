---
id: storage-graph-db-fit
node: storage.nosql
type: qa
---
## Q
What query shape justifies a graph database over a relational schema with join tables?

## A
**Variable-depth, multi-hop traversals**: "friends-of-friends-of-friends", fraud rings, dependency chains — where the number of hops isn't fixed at query time.

Relationally, each hop is another self-join whose cost grows with total edge-table size; a graph DB stores adjacency directly, so traversal cost scales with the **edges actually touched**, not the whole graph.

If your queries are fixed one/two-hop lookups ("this user's friends"), join tables with proper indexes are fine — don't pay the operational cost of a niche database for that.

## Q zh
什么查询形状证明选图数据库比关系 schema 加 join 表的成本更低？

## A zh
**可变深度、多跳遍历**："朋友的朋友的朋友"、欺诈环、依赖链——其中跳数在查询时不固定。

在关系型中，每跳是另一个自 join，其成本随总边表大小增长；图 DB 直接存储邻接，所以遍历成本按**实际触及的边**扩展，不是整个图。

如果你的查询是固定的一跳/二跳查找（"这个用户的朋友"），带适当索引的 join 表很好——不要为了这个付出小众数据库的运维成本。
