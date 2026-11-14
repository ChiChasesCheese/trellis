---
id: cbr-hm-dd-oncall
node: hm.deep-dives
type: qa
step: 7
---
## Q
项目深挖：值班与跨组件排查（可观测性 + Terraform 7 分钟根因），怎么讲？

## A
**对应 JD**：debugging and observability tools、failure analysis、shorter debugging cycles。

1. **Hook**: "I'd rather own '**here's the next one**' than just the one that paged."
2. **Observability**: transaction tracing with **Sentry** and **Datadog**, so one fee can be followed across stages.
3. **Incident**: an infra release failed in QA; root cause in **7 minutes** — `outbound_privileges` was unset, so Terraform never revoked dependent grants; same-day deploy to **three environments**.
4. **Then the class**: I **scanned the repo** — **42 of 79** similar resources lacked it; **two** real risks in another module, **flagged** to the owner.
5. **Lesson**: "Fixing one and **eliminating the class** are different jobs; keep claims as narrow as what I checked."

> 中文提示：你只是被 cc，不是被指派；先问再推 PR。追问陌生故障怎么下手：时间线 → 切片 → 一个具体案例 → 逐阶段回溯。
