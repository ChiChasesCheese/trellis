---
id: hi-pt-tt-query-condition-parser-10-index-maintain
node: tt.lld.tt-query-condition-parser.points
type: qa
step: 10
---
## Q
**条件解析与内存表查询 · 索引的维护**｜出自：条件解析与内存表查询 › 深入 4

内存表用 `dict[值, set[rowid]]` 做等值索引。插入、删除时要注意什么？`NULL` 进不进索引？

## A
**要点。** 主数据和所有索引必须一起改，删除时用旧行的值从每个索引里摘掉 rowid；并发时放在同一把锁内。

**NULL。** 不进索引：`=` 和 `IN` 永远匹配不到 `NULL`；`IS NULL` 不走这个索引。

**用 rowid。** 索引存 rowid 而不是行，一行被多个索引引用也只有一份数据。
