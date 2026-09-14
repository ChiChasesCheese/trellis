---
id: reliability-symptom-vs-cause-alerts
node: reliability.slo
type: qa
---
## Q
"Page on symptoms, ticket on causes" — what does that mean, and why does cause-based paging (CPU > 90%, disk 80% full) rot an on-call rotation?

## A
- **Symptom alerts** fire on what users experience — the SLIs behind your SLO (error rate, latency). Every page then means real or imminent user impact and maps to budget burn ([[reliability-burn-rate-alerting]]).
- **Cause alerts** fire on internal states that *might* cause impact. Most are false alarms (high CPU with healthy latency), and no finite list of causes covers every failure — so you get both noise *and* misses.

Cause signals still matter — as **dashboards and tickets** for debugging and slow-moving risks (disk filling over days), not pages. Rule: a page must be urgent, user-impacting, and actionable.

## Q zh
"在症状上页面，在原因上工单"——那意味着什么，为什么基于原因的页面（CPU > 90%，磁盘 80% 满）腐烂一个待命轮换？

## A zh
- **症状告警**在用户体验什么时触发——SLO 后面的 SLI（错误率、延迟）。然后每个页面意味着真实或迫在眉睫的用户影响并映射到预算燃烧（[[reliability-burn-rate-alerting]]）。
- **原因告警**在*可能*导致影响的内部状态时触发。大多数是虚警（高 CPU 带健康延迟），没有有限的原因列表覆盖每个故障——所以你获得噪声*和*未命中。

原因信号仍然重要——作为**仪表盘和工单**用于调试和慢动风险（磁盘在数天内填满），不是页面。规则：页面必须是紧急、用户影响和可操作的。
