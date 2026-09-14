---
id: isolation-per-workload-tuning
node: warehouse.isolation-workload-separation
type: qa
tags: [grown]
---
## Q
把 ETL、BI 看板、分析师临时查询（ad hoc）拆成三个虚拟仓库（virtual warehouse）后，每个仓库通常怎样按负载特征分别配置？

## A
ETL：批量重计算，选较大规格，跑完即挂起，auto-suspend 设短。BI 看板：大量并发的小查询，选较小规格并配多集群（multi-cluster）应对并发，auto-suspend 可略长以保留本地缓存、降低首查延迟。临时查询：负载不可预测，选中等规格，配 resource monitor（资源监控器）限额，并用 `STATEMENT_TIMEOUT_IN_SECONDS` 限制失控查询。混在一个仓库里时，这些相互矛盾的设置无法同时满足。
