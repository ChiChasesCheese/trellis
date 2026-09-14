---
id: copy-into-user-warehouse-single-txn
node: ingestion.bulk-copy-into
type: qa
source: snowflake-docs
---
## Q
用 `COPY INTO <table>` 做批量加载时，计算资源从哪来、事务怎么划分、费用怎么算？这与 Snowpipe 有何不同？

## A
批量加载使用 COPY 语句所指定的、用户自己的虚拟仓库（virtual warehouse），用户需要按预期数据量选好仓库规格，费用按仓库活跃时长计费；一次 COPY 始终在单个事务中完成，和用户手动提交的其他 SQL 一样写入表。Snowpipe 则使用 Snowflake 提供的无服务器（serverless）计算，按实际使用的计算资源计费，并会按文件中行的数量和大小把加载合并或拆分成一个或多个事务。
