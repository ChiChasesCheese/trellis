---
id: meta-bottleneck-row-by-row-dml
node: metadata.metadata-scaling-consistency
type: qa
tags: [grown]
---
## Q
把 OLTP 习惯带到 Snowflake，用循环逐行执行上万条单行 INSERT，为什么会非常慢？该怎么改？

## A
Snowflake 的每次提交都要写出新的不可变微分区（micro-partition）文件，并在元数据存储中执行一次事务来登记新的表版本。逐行提交意味着上万次文件写入和上万次元数据事务，瓶颈落在元数据层和提交路径上，而不是计算量本身，还会产生大量很小的微分区。应改为批量加载（多行 INSERT、`COPY INTO` 或 `INSERT ... SELECT`），让一次提交承载大量行。
