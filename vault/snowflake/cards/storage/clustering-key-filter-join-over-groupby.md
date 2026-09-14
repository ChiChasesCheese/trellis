---
id: clustering-key-filter-join-over-groupby
node: storage.clustering-keys
type: qa
source: snowflake-docs
---
## Q
一张事实表的查询里，`invoice_date` 常用于 WHERE 过滤，`region` 常用于 GROUP BY，聚簇键（clustering key）应优先选哪一列？为什么？

## A
优先选 `invoice_date`。聚簇键的优先顺序是：先选最常用于选择性过滤条件的列，再有余量时考虑连接（JOIN）谓词中的列；GROUP BY / ORDER BY 列有时有帮助，但通常不如过滤和连接列。原因是过滤列上的聚簇直接让大量微分区（micro-partition）被剪枝跳过，收益最大。
