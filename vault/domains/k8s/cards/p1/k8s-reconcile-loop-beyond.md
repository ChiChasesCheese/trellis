---
id: k8s-reconcile-loop-beyond
node: p1.t04.declarative-model-reconcile-loop
type: qa
step: 3
tags: [拓展]
---
## Q
**Reconcile loop · 2026 实践**｜拓展 · v1.36 beta / v1.37

controller 对比的「现在几个 Pod」来自它本地缓存的数据，缓存有可能比 API server 里的落后。落后了会出什么事？

## A
**问题（staleness）：** controller 在过时数据上做决定。官方列出三类症状：

| 症状 | 例子 |
|---|---|
| 做了错误的动作 | 缓存里还没看到刚创建的 Pod，以为少了，又补一个 |
| 该动手时没动手 | 缓存里还是旧状态，没发现差异 |
| 动作太慢 | 缓存更新晚了，修复被拖延 |

- **为什么这类 bug 难发现：** 平时缓存几乎实时，只有负载高、网络抖动时才暴露。
- **v1.36：** Kubernetes 针对 controller 的 staleness 加了缓解和可观测手段，处于 **beta**。v1.37 仍是 beta，范围扩到 HorizontalPodAutoscaler controller，并多了「熔断式」变体（node-lifecycle 这类对延迟敏感的 controller 在做破坏性决定前，直接向 API server 读一次，缓存没追上就不动手）。
- **写自己的 controller 时：** 不要假设本地缓存永远是最新的；动作要能容忍重复执行（幂等）。

**出处：** kubernetes.io 博客「Kubernetes v1.36: Staleness Mitigation and Observability for Controllers」；beta 阶段见 v1.36 发布说明；v1.37 发布博客（Stale controller mitigation，KEP-5647）
