---
id: security-optimization-observability-cost
node: security-cost.optimization
type: qa
---
## Q
Observability storage cost is rising faster than traffic. What should be reduced first without blinding on-call?

## A
Remove unused high-cardinality labels and duplicate events, shorten retention for verbose diagnostics, aggregate common metrics, and sample routine success while retaining security violations, errors, and an unbiased baseline. Tie every signal to a dashboard, alert, investigation, or audit need. Do not cut the user SLI or rollout guardrails that prove whether other cost optimizations are safe.

## Q zh
observability storage cost 的增长快于 traffic。首先应减少什么，才能不让 on-call 失明？

## A zh
删除 unused high-cardinality label 和 duplicate event，缩短 verbose diagnostic 的 retention，聚合 common metric，并 sample routine success，同时保留 security violation、error 和 unbiased baseline。让每个 signal 对应 dashboard、alert、investigation 或 audit need。不要削减 user SLI 或 rollout guardrail，因为它们用来证明其他 cost optimization 是否安全。
