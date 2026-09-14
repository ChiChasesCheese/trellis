---
id: attrib-account-usage-latency-limit
node: cost.access-history-lineage-for-cost
type: qa
tags: [grown]
---
## Q
成本归因报表基于 ACCOUNT_USAGE 的 `ACCESS_HISTORY`、`QUERY_ATTRIBUTION_HISTORY` 等视图构建。它适合做什么，不适合做什么？

## A
适合做事后诊断和周期性报表：这些视图覆盖整个账户、保留期长（约一年），能看出按周或按月的成本趋势与主要驱动因素。不适合做实时止损：视图数据有数小时级的延迟，某个失控查询正在烧钱时报表还看不到。实时防护应交给资源监控器、预算告警和语句超时等机制，归因报表负责找出根因、指导长期优化。
