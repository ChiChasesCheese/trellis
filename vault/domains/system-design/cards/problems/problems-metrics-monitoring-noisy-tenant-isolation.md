---
id: problems-metrics-monitoring-noisy-tenant-isolation
node: problems.search.metrics-monitoring
type: qa
step: 8
tags: [grown]
---
## Q
In a multi-tenant metrics monitoring system design, what two independent mechanisms prevent one tenant's misbehaving query or write burst from degrading every other tenant sharing the cluster?

## A
On the write side, per-tenant series-cardinality quotas enforced at admission time cap how many new series a single tenant can introduce, so one tenant's labeling mistake cannot consume the cluster's shared memory budget. On the query side, each query's memory usage is tracked both locally and cluster-wide, with queries that exceed a per-tenant budget cancelled outright, and query-execution threads are placed into per-tenant cgroups so CPU time is shared fairly rather than first-come-first-served. These two mechanisms are independent: the write-side quota alone would not stop an expensive query with no filters from starving other tenants' CPU and memory, and the query-side controls alone would not stop a cardinality explosion from exhausting shared storage memory.

## Q zh
在一个多租户指标监控系统设计中，哪两个独立的机制能防止一个租户失控的查询或写入突增拖慢共享同一集群的所有其他租户？

## A zh
在写入侧，准入时强制的每租户序列基数配额限制了单个租户能引入多少新序列，所以一个租户的打标签错误无法侵占集群共享的内存预算。在查询侧，每个查询的内存占用被本地和跨集群双重追踪，超出租户预算的查询直接被取消，查询执行线程被放进按租户划分的 cgroup，让 CPU 时间被公平分配而不是先到先得。这两个机制彼此独立：只有写入侧配额挡不住一个没有过滤条件的昂贵查询独占其他租户的 CPU 和内存；只有查询侧控制也挡不住一次基数爆炸耗尽共享的存储内存。
