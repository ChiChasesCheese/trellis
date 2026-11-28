---
id: hi-c-sd-data-modeling-n12-graph
node: sd.core-concepts.data-modeling.notes
type: qa
step: 12
---
## Q
**数据建模 · 图数据库**｜摘要 · 追问
图数据库在面试里值不值得选？为什么？

## A
- **是什么：** 以节点和边存数据，优化沿着关系遍历。
- **面试里几乎不选：** 经典例子是社交网络和推荐，但大型社交网络的社交关系数据也是建在 MySQL 上的。别的数据库已能应付主要查询，而专用图系统带来运维复杂度。
- **提它的后果：** 听起来高级，实际是面试常见失误，因为它增加了不必要的复杂度。例：Neo4j、Amazon Neptune。
