---
id: delivery-flags-kill-switch-scope
node: delivery.flags
type: qa
---
## Q
An image transformer is exhausting CPU. What properties make its kill switch operationally useful rather than decorative?

## A
It must be independently changeable from a deploy, propagate within a measured bound, have a safe fallback such as serving the original image, and be evaluable before expensive work starts. Scope it by feature or tenant without requiring the failing dependency, protect it with authorization and audit, test it regularly, and expose whether each worker has applied the new version.

## Q zh
image transformer 正在耗尽 CPU。什么特性让它的 kill switch 真正可运维，而不是装饰？

## A zh
它必须能独立于 deploy 修改、在测量过的时间上限内传播、具备安全 fallback（例如返回 original image），并在 expensive work 开始前完成 evaluation。它应能按 feature 或 tenant 限定 scope，而不依赖正在失败的 dependency；同时具备 authorization、audit、定期测试，并暴露每个 worker 是否已应用新 version。
