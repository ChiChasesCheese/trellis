---
id: analytics-columnar-compression
node: analytics.olap
type: qa
---
## Q
Name the two compression tricks that make columnar storage so effective, and why sorting the column first multiplies their effect.

## A
- **Dictionary encoding**: replace repeated values with small integer codes (a `country` column becomes 1–2 bytes per row).
- **Run-length / bitmap encoding**: store "value X repeats N times" or one bitmap per distinct value — a bitmap over a low-cardinality column also turns `WHERE` predicates into fast bitwise AND/ORs.

Sorting first puts equal values **adjacent**, turning millions of rows into a handful of runs. The catch: you only get one sort order per copy, so systems keep the sort key aligned with the most common filter (or store multiple sort orders across replicas).

## Q zh
列举使列存储如此有效的两个压缩技巧，以及为什么先对列排序会乘以它们的效果。

## A zh
- **Dictionary 编码**：用小整数代码替换重复值（一个`country`列变成每行 1–2 字节）。
- **Run-length / bitmap 编码**：存储"值 X 重复 N 次"或每个不同值一个 bitmap — 低基数列上的 bitmap 也把`WHERE`谓词变成快速按位与/或。

先排序把相等值**放在相邻**，把数百万行变成少数 run。捕捉：每个副本只能得到一个排序顺序，所以系统保持排序 key 对齐最常见过滤（或存储跨副本的多个排序顺序）。
