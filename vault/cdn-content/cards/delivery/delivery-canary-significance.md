---
id: delivery-canary-significance
node: delivery.canary
type: qa
---
## Q
A canary shows a statistically significant 0.2 ms p50 improvement and a noisy 8% p99 regression. Should it advance?

## A
No. Practical impact and risk dominate a tiny p50 win: investigate the tail regression and extend the sample across expected traffic cycles. Predefine decision metrics and minimum meaningful effects so repeated dashboard watching does not cherry-pick significance. For a content path, correctness and SLO guardrails are vetoes even when an aggregate performance metric improves.

## Q zh
canary 显示 statistically significant 的 0.2 ms p50 improvement，同时 p99 有 noisy 8% regression。应该继续推进吗？

## A zh
不应该。practical impact 和 risk 比微小的 p50 收益更重要：应调查 tail regression，并延长 sample 覆盖预期 traffic cycle。预先定义 decision metric 和 minimum meaningful effect，避免反复看 dashboard 后 cherry-pick significance。对于 content path，即使 aggregate performance metric 改善，correctness 和 SLO guardrail 仍具有 veto 权。
