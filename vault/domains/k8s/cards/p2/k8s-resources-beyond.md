---
id: k8s-resources-beyond
node: p2.t04.resource-requests-limits-qos-classes
type: qa
step: 3
tags: [拓展]
---
## Q
**Pod-level resources · 2026 实践**｜拓展 · v1.34 beta

一个 Pod 里有主容器和两个辅助容器，每个容器分别写 requests 和 limits 很繁琐。有没有办法对整个 Pod 设一个总量？QoS class 怎么算？

## A
**Pod-level resources：** 直接在 Pod 的 `spec.resources` 上写 requests 和 limits，作为整个 Pod 的预算，容器共享这份预算。**v1.34 beta**。

| | 容器级 | Pod 级（beta） |
|---|---|---|
| 写在哪 | 每个容器的 `resources` | Pod 的 `spec.resources` |
| 好处 | 精确控制每个容器 | 多个容器共用一份总量，辅助容器不用单独估 |
| Guaranteed 条件 | 每个容器的 CPU、内存 request = limit | Pod 级的 CPU、内存 request = limit |

- **QoS：** 用了 Pod 级资源，Guaranteed 的条件改成看 Pod 级的 request 和 limit。
- **配合 in-place resize：** Pod 级资源的原地调整是 v1.36 beta（第 7 部分）。
- **何时用：** sidecar 多、各自用量波动大的 Pod。

**出处：** kubernetes.io 发布博客 v1.34（Pod-level resources，KEP-2837，beta）、v1.36；kubernetes.io Concepts › Pod Quality of Service Classes
