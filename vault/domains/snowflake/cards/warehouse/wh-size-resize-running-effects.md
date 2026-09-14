---
id: wh-size-resize-running-effects
node: warehouse.sizing-t-shirt
type: qa
source: snowflake-docs
---
## Q
一条查询正在虚拟仓库（virtual warehouse）上慢慢跑，此时把仓库调大，这条查询会加速吗？从 6X-Large 调小到 4X-Large 时计费上有什么特殊之处？

## A
不会。仓库可以在运行中随时调整规格，但新增的计算资源不影响已在执行的查询，只有在完全就绪后才供排队中和新提交的查询使用；新增资源从调整时刻起计费。从 5X-Large 或 6X-Large 调到 4X-Large 或更小时，会有一小段时间同时按新旧两套仓库计费，因为旧仓库需要先静默（quiesce）结束。
