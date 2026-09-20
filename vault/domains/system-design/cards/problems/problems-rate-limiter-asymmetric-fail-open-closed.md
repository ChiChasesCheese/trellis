---
id: problems-rate-limiter-asymmetric-fail-open-closed
node: problems.foundations.rate-limiter
type: qa
step: 6
tags: [grown]
---
## Q
In a rate limiter with both per-key fairness limits and a global fleet-protection limit, why does the design fail open for the per-key layer but fail closed (in a degraded, self-tracked form) for the fleet layer when the central counter store becomes unreachable?

## A
The two layers protect different things. The per-key layer's job is fairness between callers — losing exact enforcement briefly and letting some extra traffic through is a small cost compared to turning a rate-limiter outage into an API availability incident, so it fails open. The fleet layer's job is protecting the backend from being overwhelmed at all, which is not a cost worth trading away even during a central-store outage, so each gateway node keeps enforcing a degraded limit based on its own recently observed admitted traffic rather than admitting everything unconditionally. The general principle: the layer closer to the user, whose purpose is fairness, favors availability on failure; the layer closer to backend protection, whose purpose is self-preservation, favors staying conservative on failure.

## Q zh
在一个既有 per-key 公平性限制、又有全局 fleet 自保限制的速率限制器里，为什么中心计数器存储不可达时，per-key 层选择 fail-open，而全局 fleet 层选择（以本地自主追踪的方式）保守退化，而不是同样 fail-open？

## A zh
这两层保护的目标不同。per-key 层的职责是调用方之间的公平性——短暂失去精确执行、放行一些额外流量，代价远小于把一次限流器故障变成一场 API 可用性事故，所以它 fail-open。fleet 层的职责是保护后端完全不被打垮，这个目标不值得在中心存储故障时被牺牲，所以每个网关节点会基于自己最近观测到的放行流量继续执行一个退化版本的限制，而不是无条件放开。一般原则是：离用户更近、目的是公平性的那一层，故障时偏向可用性；离后端保护更近、目的是自保的那一层，故障时偏向保守。
