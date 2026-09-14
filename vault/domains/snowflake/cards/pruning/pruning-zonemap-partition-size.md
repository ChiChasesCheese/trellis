---
id: pruning-zonemap-partition-size
node: pruning.min-max-zone-maps
type: qa
source: snowflake-docs
---
## Q
Snowflake 的微分区（micro-partition）大小被设计为多大，这个大小选择和 zone map 剪枝效果之间是什么关系？

## A
每个微分区未压缩时约为 50MB–500MB（实际压缩后更小）。分区越小，min/max 范围越窄、越不容易和查询谓词的范围重叠，剪枝的粒度就越细；但分区太小会导致元数据数量爆炸、元数据管理和扫描调度的开销上升。50–500MB 是在“剪枝粒度”和“元数据开销”之间的折中。
