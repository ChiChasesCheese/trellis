---
id: hi-pt-credit-token-balance-4-sort-key
node: qb.lld.credit-token-balance.points
type: qa
step: 4
---
## Q
**额度账本 · 排序键与同刻规则**｜必会 · 出自：额度账本 › 深入 2

重放的事件按什么键排序？同一时刻既有发放又有扣费、或两笔同时到期，谁先？

## A
**事件键。** `(at, isinstance(e, Charge), id)`：同一时刻先发放后扣费，保证发放时刻就能用；`id` 兜底，结果与到达顺序无关。

**包键。** 同一时刻到期的，先发放的先扣，再按 `id`。

**区间。** 发放时刻含、到期时刻不含：第 2 天到期的包与第 2 天生效的包，第 2 天余额只算后者。
