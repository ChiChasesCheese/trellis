---
id: reliability-retry-storm
node: reliability.resilience.retries
type: qa
---
## Q
A service slows down, clients retry, and the service dies completely. Name the failure mode and three design rules that prevent it.

## A
**Retry storm** — retries multiply offered load exactly when capacity is lowest (3 layers each retrying 3x = 27x amplification).

- **Exponential backoff with jitter** so retries spread out instead of synchronizing.
- **Retry budgets** (e.g. retries ≤ 10% of requests) and retry only at one layer, not every hop.
- **Circuit breakers / load shedding** so callers fail fast instead of piling on — and only retry idempotent operations.

## Q zh
一个服务变慢，客户端重试，服务完全死亡。命名故障模式和三个阻止它的设计规则。

## A zh
**Retry storm** ——重试在容量最低时正好乘以提供负载（3 层每个重试 3 倍 = 27 倍放大）。

- **带抖动的指数退避**所以重试分散而不是同步。
- **Retry budget**（例如重试 ≤ 10% 的请求）和仅在一层重试，不是每个 hop。
- **Circuit breaker / load shedding** 所以调用者快速失败而不是堆积——仅重试幂等操作。
