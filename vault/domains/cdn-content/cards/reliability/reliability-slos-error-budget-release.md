---
id: reliability-slos-error-budget-release
node: reliability.slos
type: qa
---
## Q
The service has consumed 80% of its monthly error budget in four days, and a cache-key optimization is ready to ship. What decision should the error budget drive?

## A
Pause broad rollout and spend the remaining budget on stabilizing the current path. The change may still proceed only as a tightly bounded canary if it directly mitigates the burn, has explicit stop conditions, and can be reversed immediately. Error budget is a change-governance signal, not permission to consume the final 20% because the calendar month is young.

## Q zh
服务在四天内消耗了月度 error budget 的 80%，同时一个 cache-key optimization 已准备发布。error budget 应驱动什么决策？

## A zh
暂停 broad rollout，把剩余 budget 用于稳定当前 path。只有当该 change 能直接降低 burn、采用严格限制的 canary、具有明确 stop condition，并可立即 reverse 时，才应继续。error budget 是 change-governance signal，不是因为月初就可以继续消耗最后 20% 的许可。
