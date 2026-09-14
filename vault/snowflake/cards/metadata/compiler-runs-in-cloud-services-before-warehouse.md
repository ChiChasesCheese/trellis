---
id: compiler-runs-in-cloud-services-before-warehouse
node: metadata.query-compiler-pipeline
type: qa
tags: [grown]
---
## Q
一条 SELECT 提交到 Snowflake 后，解析（parse）、绑定（bind）、优化（optimize）是在虚拟仓库（virtual warehouse）上做，还是在别处？这对排查“查询慢”意味着什么？

## A
这三步都在云服务（Cloud Services）层完成，完成后才把物理执行计划交给虚拟仓库执行。因此一条查询的总耗时要拆开看：`QUERY_HISTORY` 中的 COMPILATION_TIME 反映云服务层的编译耗时，排队时间反映等待仓库资源，EXECUTION_TIME 才是仓库上的执行耗时。编译慢靠加大仓库解决不了，因为编译根本不在仓库上运行。
