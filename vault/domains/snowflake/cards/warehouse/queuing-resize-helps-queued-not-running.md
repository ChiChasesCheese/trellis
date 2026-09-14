---
id: queuing-resize-helps-queued-not-running
node: warehouse.query-queuing
type: qa
source: snowflake-docs
---
## Q
仓库已经有若干查询在跑、另有一批在排队，这时把虚拟仓库（virtual warehouse）调大，哪些查询能受益？

## A
只有排队中的和新提交的查询能受益。新增的计算资源完全就绪之后，才会分配给排队和新来的查询；已经在执行的查询不会被加速，仍使用它们开始时预留的资源。
