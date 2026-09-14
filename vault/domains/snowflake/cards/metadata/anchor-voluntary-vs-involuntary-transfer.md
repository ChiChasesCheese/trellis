---
id: anchor-voluntary-vs-involuntary-transfer
node: metadata.execution-anchor
type: qa
tags: [grown]
---
## Q
执行锚点（execution anchor）所在的云服务实例“繁忙或要下线”与“突然崩溃”这两种情况，查询所有权的转移路径有何本质不同？

## A
繁忙或计划下线（例如滚动升级时排空实例）走主动转移（voluntary transfer）：原锚点实例仍然存活，可以有序地把查询的控制权交给另一个实例，并确认对方接手后再放手，交接双方都清楚状态。突然崩溃走被动转移（involuntary transfer）：原实例无法配合，只能由系统检测到它失联后，由其他实例依据共享元数据中记录的查询状态接管，或判定查询失败后重试。被动路径必须防范“原实例其实没死”的情况，避免出现两个锚点。
