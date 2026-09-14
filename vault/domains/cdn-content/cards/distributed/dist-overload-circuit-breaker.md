---
id: dist-overload-circuit-breaker
node: distributed.overload
type: qa
---
## Q
What failure does a circuit breaker prevent, and why must its half-open state be tightly limited?

## A
It stops repeatedly spending threads, connections, and deadlines on a dependency with a high recent failure rate, enabling fast fallback or rejection. After a cool-down, half-open admits only a few probes; if all traffic returns at once, the recovering dependency is re-overloaded and the fleet synchronizes another failure. Add jitter, per-destination state, and observability; do not use the breaker to hide permanent application errors.

## Q zh
circuit breaker 防止什么 failure？为什么 half-open 状态必须严格限流？

## A zh
它阻止系统反复把 thread、connection 和 deadline 浪费在近期高失败率的 dependency 上，从而快速 fallback 或 reject。cool-down 后，half-open 只允许少量 probe；若全部流量一次性恢复，正在恢复的 dependency 会再次 overload，fleet 也会同步制造下一次故障。需要 jitter、per-destination state 与 observability；不要用 breaker 掩盖永久 application error。
