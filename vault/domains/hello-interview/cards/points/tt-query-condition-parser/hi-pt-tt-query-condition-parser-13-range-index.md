---
id: hi-pt-tt-query-condition-parser-13-range-index
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 13
---
## Q
**条件解析与内存表查询 · 范围查询怎么走索引**｜出自：条件解析与内存表查询 › 取舍与追问

`age > 18` 用不上哈希索引。数据量大时怎么办？

## A
**要点。** 换成有序结构：用 `bisect` 维护 `(值, rowid)` 的有序列表，查询 `O(log n + 结果数)`，插入 `O(n)`；真实数据库用 B+ 树，插入和查询都是 `O(log n)`。

**取舍。** 写多的表索引越多越慢，只给高频查询的字段建。
