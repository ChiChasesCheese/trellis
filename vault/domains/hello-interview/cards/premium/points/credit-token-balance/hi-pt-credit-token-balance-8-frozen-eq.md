---
id: hi-pt-credit-token-balance-8-frozen-eq
node: qb.lld.credit-token-balance.points
type: qa
step: 8
---
## Q
**额度账本 · 冻结事件的按值比较**｜追问 · 出自：额度账本 › 逐步扩展 1

幂等判断"是不是同样的参数"代码里只有一句 `old != new`。事件对象要做成什么样才行？

## A
**做法。** 事件是 `@dataclass(frozen=True, slots=True)`：自带按值比较，所以 `old != new` 逐字段比较；不可变，别处改不了它。

**效果。** `dataclasses.replace(grant, expires_at=at)` 能生成改过到期时间的副本（作废就用它）。

**对比。** 可变对象要手写比较，并防着别处改它（不可变事件）。
