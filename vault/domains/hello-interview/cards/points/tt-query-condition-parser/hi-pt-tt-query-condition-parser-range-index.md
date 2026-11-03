---
id: hi-pt-tt-query-condition-parser-range-index
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 13
---
## Q
**条件解析与内存表查询 · 范围查询怎么走索引**｜加分 · 出自：条件解析与内存表查询 › 深入 4

`age > 18` 用不上哈希索引，数据量大时怎么办？

## A
**要点。** 用 `bisect` 维护 `(值, 行)` 的有序列表，查询 `O(log n + 结果数)`，插入 `O(n)`；真实数据库用 B+ 树。

**取舍。** 索引越多写越慢，只给高频查询的字段建。
