---
id: hi-pt-dasher-payout-11-settlement
node: qb.lld.dasher-payout.points
type: qa
step: 11
---
## Q
**配送员报酬计算 · 结算周期归属**｜加分 · 出自：配送员报酬计算 › 深入 7

按周结算：一单从周日 23:50 接单、周一 00:20 送达，记入哪一周？为什么不按每段发生的时间拆？

## A
**选择。** 整单记入结束时间落在 `[start, end)` 内的那一期，所以记入周一所在的周。

**为什么。** 按每段发生的时间拆，同一单会落到两个周期，对账和配送员看到的单据都对不上。代价是跨天的单在结束那天一次性入账。

```python
return sum((pays[d.id] for d in ds if start <= d.ended < end), Decimal("0.00"))
```
