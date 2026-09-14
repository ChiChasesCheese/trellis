---
id: result-cache-exact-text-match
node: cache.result-cache
type: qa
source: snowflake-docs
---
## Q
两次提交的 SQL 在逻辑上等价，但一次用了小写关键字、另一次用了大写关键字，或者一次给表加了别名（alias）、另一次没加，这两次查询能命中同一条持久化结果缓存吗？为什么？

## A
不能。结果缓存要求新查询与此前执行过的查询在文本上完全一致，任何书写差异——包括大小写、是否使用表别名——都会被视为不同的查询，从而使缓存失效，因为 Snowflake 判断是否命中缓存是基于 SQL 文本本身，而不是基于其语义等价性。
