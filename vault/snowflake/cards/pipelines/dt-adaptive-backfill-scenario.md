---
id: dt-adaptive-backfill-scenario
node: pipelines.dynamictable-adaptive-refresh
type: qa
source: snowflake-docs
---
## Q
上游事实表平时每小时只追加少量数据，但每月一次会整体回填重写过去一年的数据。对依赖它的动态表，INCREMENTAL 和 ADAPTIVE 各会表现如何？

## A
纯 INCREMENTAL 模式在回填那次仍会尝试逐行计算一年量级的变化，刷新可能极慢，导致实际延迟远超目标延迟。ADAPTIVE 模式平时同样走增量、成本低；遇到回填时检测到大规模上游变化，自动重新初始化，避免低效的超大增量计算。这类「平时小变化、偶尔大变化」的负载正是 ADAPTIVE 的典型场景。
