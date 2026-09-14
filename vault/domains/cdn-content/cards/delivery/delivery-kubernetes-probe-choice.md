---
id: delivery-kubernetes-probe-choice
node: delivery.terraform-kubernetes
type: qa
---
## Q
A cache pod cannot reach origin for 10 seconds but can still serve HITs and stale content. Should its liveness probe fail?

## A
Usually no. Liveness should fail only when restarting the process can repair it; dependency failure may make restarts amplify the incident and erase warm cache. Readiness may reflect whether the pod can satisfy its serving contract, possibly remaining ready for HIT/stale traffic while metrics expose degraded origin access. Use startup probes for slow warm-up and keep probe logic local and bounded.

## Q zh
cache pod 有 10 秒无法访问 origin，但仍能提供 HIT 和 stale content。它的 liveness probe 应失败吗？

## A zh
通常不应该。只有 restart process 能修复的问题才应让 liveness fail；dependency failure 下反复 restart 可能放大 incident，并清空 warm cache。readiness 应反映 pod 是否能满足 serving contract；如果还能提供 HIT/stale traffic，它可以保持 ready，同时用 metric 暴露 degraded origin access。slow warm-up 使用 startup probe，probe logic 应 local 且 bounded。
