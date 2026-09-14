---
id: scale-out-max-clusters-budget
node: warehouse.scaling-up-vs-out
type: qa
source: snowflake-docs
---
## Q
给一个 X-Large（每集群每小时 16 credit）多集群仓库（multi-cluster warehouse）设置最大集群数时，应如何权衡？设为 10 的最坏情况每小时花多少？

## A
最大集群数应在留意规格和相应 credit（信用点）成本的前提下尽量设大，好让并发高峰时能扩出足够的集群。最坏情况是 10 个集群整小时全部运行：16 × 10 = 160 credit/小时。在 Auto-scale 模式下只有负载需要时才会真正拉起这些集群，所以上限是预算保护线，而非日常花费。
