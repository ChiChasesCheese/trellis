---
id: reliability-circuit-breaker-states
node: reliability.resilience.containment
type: qa
---
## Q
What problem does a circuit breaker solve that per-request timeouts and retries do not, and how do its three states work?

## A
Timeouts protect one call; a breaker protects the **caller's capacity** — when a dependency is down, threads/connections stop being wasted on calls that are doomed, and the dependency gets room to recover.

- **Closed**: normal traffic; failures counted.
- **Open**: failure rate tripped the threshold; calls fail fast (or serve fallback) without hitting the dependency.
- **Half-open**: after a cooldown, a few probe requests pass; success closes it, failure reopens it.

## Q zh
Circuit breaker 解决什么问题而 per-request timeout 和 retry 做不到，它的三个状态是如何工作的？

## A zh
Timeout 保护一个调用；breaker 保护**调用者的容量** ——当依赖宕机时，线程/连接停止在注定失败的调用上浪费，依赖获得恢复的空间。

- **Closed**：正常流量；故障计数。
- **Open**：故障率触发阈值；调用快速失败（或提供 fallback）而不打到依赖。
- **Half-open**：冷却后，几个探针请求通过；成功则关闭，失败则重新打开。
