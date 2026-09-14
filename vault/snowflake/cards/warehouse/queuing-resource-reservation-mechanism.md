---
id: queuing-resource-reservation-mechanism
node: warehouse.query-queuing
type: qa
source: snowflake-docs
---
## Q
Snowflake 虚拟仓库（virtual warehouse）能同时跑多少条查询是固定的吗？查询在什么时刻、因为什么原因进入排队？

## A
不是固定数值，而是由每条查询的大小和复杂度决定。查询提交时，仓库会计算并预留执行它所需的计算资源；如果仓库剩余资源不足以处理这条查询，它就进入排队，等其他正在运行的查询完成、释放出资源后再执行。所以几条重查询就可能占满仓库，让后续的轻查询也排队。
