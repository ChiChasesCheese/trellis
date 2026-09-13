---
id: reliability-alerting-multiwindow-burn
node: reliability.alerting
type: qa
---
## Q
Why combine a fast and a slow error-budget burn window instead of paging on a single five-minute error-rate threshold?

## A
The fast window detects severe new failures quickly, while the slow window confirms the burn is sustained relative to the SLO. Requiring both reduces pages for brief noise without waiting hours on a real outage. Thresholds should express budget consumption rate, not a universal raw error percentage, so they remain aligned with the service objective.

## Q zh
为什么要组合 fast 和 slow error-budget burn window，而不是只对 five-minute error-rate threshold 发 page？

## A zh
fast window 能快速发现严重的新 failure，slow window 则确认 burn 相对 SLO 持续存在。同时满足两者，可以减少短暂 noise 的 page，又不会让真实 outage 等待数小时。threshold 应表达 budget consumption rate，而不是通用 raw error percentage，从而始终与 service objective 对齐。
