---
id: hi-pt-recently-viewed-items-4-outer-lru
node: qb.lld.recently-viewed-items.points
type: qa
step: 5
---
## Q
**"最近浏览"记录 · 外层 LRU 限制客户数**｜追问 · 出自："最近浏览"记录 › 逐步扩展 1

"最近浏览"每位客户至多 limit 条，但客户有上亿时内存仍放不下。怎么给内存上界？

## A
**要点。** 外层 customer → 有序字典也做成 LRU，限制活跃客户数，挤出最久不活跃的客户。
**回源。** 被挤出的客户数据回源到持久层；真实系统更常见的是直接放 Redis。
**组合。** 这是 LRU 套 LRU。
