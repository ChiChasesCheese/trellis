---
id: delivery-canary-ramp-guardrail
node: delivery.canary
type: qa
---
## Q
What should determine a `1% → 10% → 50% → 100%` ramp instead of a fixed timer?

## A
Advance only after a minimum sample and bake time cover the relevant cache lifecycle, while canary versus control stays inside predeclared user-SLI, correctness, saturation, and cost guardrails. Hold when evidence is inconclusive; rollback on a stop condition. Percentages are exposure controls, not evidence—each stage must answer what new scale or heterogeneity it validates.

## Q zh
什么应该决定 `1% → 10% → 50% → 100%` 的 ramp，而不是固定 timer？

## A zh
只有在 minimum sample 和 bake time 覆盖相关 cache lifecycle，且 canary 相对 control 始终处于预先声明的 user-SLI、correctness、saturation 与 cost guardrail 内时，才前进。证据不充分就 hold；触发 stop condition 就 rollback。percentage 只是 exposure control，不是 evidence；每个 stage 都必须说明它验证了哪种新 scale 或 heterogeneity。
