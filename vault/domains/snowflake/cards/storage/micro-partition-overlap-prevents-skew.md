---
id: micro-partition-overlap-prevents-skew
node: storage.micro-partition-format
type: qa
source: snowflake-docs
---
## Q
为什么 Snowflake 允许不同微分区（micro-partition）的列值范围相互重叠，这不是会让剪枝变差吗？它换来了什么？

## A
允许重叠意味着切分边界不必按某个键的取值来划分，只需按统一的小尺寸（未压缩 50–500 MB）切块。这样热门取值再多也只是多几个同样大小的分区，从而避免了按值划分分区时常见的倾斜（skew）。代价是重叠越多，一个谓词能排除的分区越少，所以对剪枝要求高的大表需要额外关注聚簇状态。
