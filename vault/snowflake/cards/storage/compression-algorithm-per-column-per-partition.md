---
id: compression-algorithm-per-column-per-partition
node: storage.columnar-compression-encoding
type: qa
source: snowflake-docs
---
## Q
Snowflake 表的压缩算法是按表选、按列选，还是更细？为什么选择粒度会细到这个程度？

## A
比按列更细：Snowflake 会为每个微分区（micro-partition，50–500 MB 未压缩数据的存储单元）中的每一列分别自动确定最高效的压缩算法。同一列在不同微分区里的数据分布可能差别很大（比如早期分区里某列几乎全是空值，后期分区取值很分散），逐分区逐列选择才能让每一块数据都用上最合适的压缩方式。
