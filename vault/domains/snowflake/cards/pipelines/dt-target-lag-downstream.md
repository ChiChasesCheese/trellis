---
id: dt-target-lag-downstream
node: pipelines.dynamictable-target-lag
type: qa
source: snowflake-docs
---
## Q
在 `dt_orders → dt_orders_daily` 这样的动态表管道里，中间表 `dt_orders` 为什么常常设置 `TARGET_LAG = DOWNSTREAM`？

## A
`DOWNSTREAM` 表示该表没有自己的新鲜度目标，只在下游依赖它的动态表需要新数据时才刷新。中间表单独按固定延迟刷新可能做无用功；设为 DOWNSTREAM 后，由最终面向用户的表（如 `dt_orders_daily`）的目标延迟驱动整条链路按需刷新，从而减少多余的刷新计算。
