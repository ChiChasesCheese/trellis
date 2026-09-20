---
id: problems-metrics-monitoring-cardinality-admission-quota
node: problems.search.metrics-monitoring
type: qa
step: 4
tags: [grown]
---
## Q
In a metrics monitoring system design, why should a per-tenant series-cardinality quota be enforced at the ingestion router at write-admission time, rather than relying on monitoring the cluster and cleaning up after a cardinality spike is discovered?

## A
By the time a cardinality spike is discovered through monitoring, the cluster has often already exhausted memory in its in-memory head-block storage, because each new label combination creates a brand-new series that must be tracked — the failure and the detection happen at roughly the same moment. Enforcing a quota at admission time means the ingestion router rejects new series that would push a tenant over its budget and returns an explicit error to the caller, so a labeling mistake is caught the instant it is introduced, scoped to one tenant, and never gets the chance to consume unbounded memory across the whole cluster.

## Q zh
在一个指标监控系统设计中，为什么应该在写入路由（ingestion router）的写入准入（admission）时刻，就对每个租户的序列基数强制配额，而不是靠监控集群、在发现基数暴涨后再清理？

## A zh
等到通过监控发现基数暴涨时，集群往往已经因为内存驻留的头块（head block）存储耗尽而出问题了——因为每一个新的标签组合都会创建一条全新的序列并被持续追踪，故障和被发现几乎同时发生。在准入时刻强制配额意味着写入路由会拒绝会让某个租户超出预算的新序列，并向调用方返回明确错误，这样打错标签这类问题在被引入的那一刻就被拦住、影响范围被限定在一个租户内，永远不会有机会在整个集群上无限制消耗内存。
