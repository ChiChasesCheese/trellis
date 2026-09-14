---
id: reliability-error-budget-throttle
node: reliability.slo
type: qa
---
## Q
Your SLO is 99.9% monthly success rate. What is the error budget, and what concretely changes when it is exhausted?

## A
Budget = 1 − SLO = **0.1% of requests** (or ~43 minutes of full downtime) per month, deliberately spendable on releases, experiments, and planned risk.

When exhausted: **feature releases freeze**; engineering shifts to reliability work until the budget refills. This turns "how reliable is reliable enough" from an argument into a pre-agreed, self-enforcing policy between product and ops.

## Q zh
你的 SLO 是每月 99.9% 成功率。error budget 是什么，当它耗尽时具体变化什么？

## A zh
Budget = 1 − SLO = **0.1% 的请求**（或每月 ~43 分钟完全停机），故意可花在发布、实验和计划风险上。

当耗尽：**功能发布冻结**；工程转向可靠性工作直到预算重填。这把"多可靠才够可靠"从论证变成产品和运维之间的预先同意、自我强制的政策。
