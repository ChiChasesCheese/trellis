---
id: meta-concurrent-writes-same-table
node: metadata.metadata-scaling-consistency
type: qa
tags: [grown]
---
## Q
多个会话同时对同一张 Snowflake 表执行 UPDATE / DELETE / MERGE，为什么吞吐上不去，而同时往不同表写入就没问题？

## A
强一致性要求对同一张表的每次提交都基于它的最新版本，并在元数据中原子地推进这张表的版本。并发修改同一张表的语句因此必须串行化：后来的语句要等锁或在冲突时重试，彼此等待。写不同的表则推进的是不同表的版本、互不冲突，可以并行提交。所以单表高并发改写是元数据一致性模型下的天然瓶颈，适合改成攒批的集中写入。
