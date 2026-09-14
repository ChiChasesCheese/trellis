---
id: wh-size-table-bytes-over-rows
node: warehouse.sizing-t-shirt
type: qa
source: snowflake-docs
---
## Q
估算一个虚拟仓库（virtual warehouse）需要多大时，应该更关注表的行数还是表的总数据量？还有哪些因素，以及为什么建议同一仓库上跑相似的查询？

## A
更关注表的总数据量，它比行数对处理量的影响更大；过滤谓词和查询中连接（join）的表数量也会影响所需资源。建议在同一个仓库上运行复杂度和数据集大致同质的查询：若混跑复杂度差异很大的查询，就很难分析仓库负载，也就很难选出与工作负载相匹配的规格。
