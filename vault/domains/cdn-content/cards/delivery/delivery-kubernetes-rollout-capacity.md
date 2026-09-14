---
id: delivery-kubernetes-rollout-capacity
node: delivery.terraform-kubernetes
type: qa
---
## Q
A Kubernetes rolling update of cache pods causes origin overload even though `maxUnavailable: 0`. What setting or behavior was overlooked?

## A
New pods may be ready before their caches are warm, while `maxSurge` adds cold capacity that generates misses rather than useful cache capacity. Gate readiness on the minimum serving capability, warm deliberately, limit concurrent cold pods, and reserve origin headroom. HPA based only on CPU can worsen the loop; observe miss rate, origin concurrency, and rollout cohort state.

## Q zh
cache pod 的 Kubernetes rolling update 导致 origin overload，尽管设置了 `maxUnavailable: 0`。忽略了什么 setting 或 behavior？

## A zh
new pod 可能在 cache warm 前就 ready，而 `maxSurge` 增加的是会产生 miss 的 cold capacity，不是有用 cache capacity。应以 minimum serving capability gate readiness，有计划地 warm，限制 concurrent cold pod，并预留 origin headroom。只基于 CPU 的 HPA 可能加剧循环；应观察 miss rate、origin concurrency 和 rollout cohort state。
