---
id: scale-up-resize-mid-batch
node: warehouse.scaling-up-vs-out
type: qa
source: snowflake-docs
---
## Q
一批规模和复杂度相近的查询要在同一个虚拟仓库（virtual warehouse）上依次运行，第一条就很慢。此时在运行中调大仓库值得吗？要注意什么？

## A
对后续查询通常值得：仓库支持在运行中随时调整规格，新增资源就绪后会供排队和新提交的查询使用。但要注意：正在跑的那条查询不会因此变快；如果这些查询本身是已经很快的小查询，调大后未必有明显提升；从 5X-Large/6X-Large 调到 4X-Large 或更小时，旧仓库静默（quiesce）期间会短暂地同时为新旧两套仓库计费。
