---
id: hi-pt-tt-per-merchant-rate-limit-2-decision-api
node: tt.lld.tt-per-merchant-rate-limit.points
type: qa
step: 2
---
## Q
**按商户限流 · 判定结果与类划分**｜必会 · 出自：按商户限流 › 核心实体与接口

`allow(merchant, cost)` 返回什么？类怎么划分，哪些是不可变的？

## A
**返回。** 不可变的 `Decision(allowed, remaining, retry_after)`，被拒时 `retry_after` 用于 Retry-After。
**类。** `Limit(rate, burst)` 不可变；`Bucket(tokens, updated)` 只有两个字段；`_Shard` 是一把锁加一个 OrderedDict（哈希表加双向链表，队头最久没用）；`MerchantRateLimiter` 持有配置、默认值、时钟和若干分段，按商户哈希选分段。
