---
id: reliability-alerting-hit-ratio-page
node: reliability.alerting
type: qa
---
## Q
Cache hit ratio drops 20%, but user latency and error SLOs remain healthy and origin has headroom. Should this page the on-call engineer?

## A
No. Treat it as a diagnostic or cost alert unless it is rapidly approaching a user-visible or capacity failure. Page on symptoms or imminent exhaustion that require urgent action, such as multi-window SLO burn or origin saturation. A hit-ratio alert needs a runbook and a clear path from threshold to action; otherwise it creates noise.

## Q zh
cache hit ratio 下降 20%，但 user latency 和 error SLO 仍健康，origin 也有 headroom。应该 page on-call engineer 吗？

## A zh
不应该。除非它正快速逼近 user-visible failure 或 capacity failure，否则应把它作为 diagnostic 或 cost alert。page 应基于需要紧急处理的 symptom 或 imminent exhaustion，例如 multi-window SLO burn 或 origin saturation。hit-ratio alert 必须有 runbook，并明确 threshold 如何触发 action；否则只会制造 noise。
