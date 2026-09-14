---
id: auto-recluster-serverless-nonblocking
node: storage.automatic-reclustering
type: qa
source: snowflake-docs
---
## Q
给一张 Snowflake 表定义聚簇键（clustering key）后，自动聚簇（Automatic Clustering）在哪里运行、何时运行、会不会挡住正在写入的 DML？

## A
它在 Snowflake 内部管理的后台无服务器（serverless）资源上运行，不需要你指定虚拟仓库（virtual warehouse）。Snowflake 随 DML 持续评估表的聚簇状态，只在表能从重新聚簇中受益时才触发，所以定义键之后不一定立刻开始。重新聚簇对用户透明，不阻塞针对该表的 DML 语句。
