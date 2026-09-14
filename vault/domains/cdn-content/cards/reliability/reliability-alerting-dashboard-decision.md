---
id: reliability-alerting-dashboard-decision
node: reliability.alerting
type: qa
---
## Q
A rollout dashboard shows only fleet-average CPU and request rate. What panels are missing before it can support a cache change decision?

## A
Add user SLI/error-budget burn, latency distributions, errors, saturation, cache outcomes by tier, origin load, revalidation/collapse behavior, and cost-relevant bytes or requests. Break down by rollout cohort and region, and annotate deploy/config changes. The dashboard must let an operator compare control with canary and decide continue, hold, or rollback.

## Q zh
rollout dashboard 只有 fleet-average CPU 和 request rate。要支持 cache change decision，还缺哪些 panel？

## A zh
应增加 user SLI/error-budget burn、latency distribution、error、saturation、按 tier 的 cache outcome、origin load、revalidation/collapse behavior，以及与成本相关的 byte 或 request。按 rollout cohort 和 region 切分，并标注 deploy/config change。dashboard 必须让 operator 比较 control 与 canary，并决定 continue、hold 或 rollback。
