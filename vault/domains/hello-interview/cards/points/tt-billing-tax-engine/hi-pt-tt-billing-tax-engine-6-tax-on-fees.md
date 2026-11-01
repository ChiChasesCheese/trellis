---
id: hi-pt-tt-billing-tax-engine-6-tax-on-fees
node: tt.lld.tt-billing-tax-engine.points
type: qa
step: 6
---
## Q
**计费与计税引擎 · 税建在费用之上**｜出自：计费与计税引擎 › 整体设计

计费引擎里"税算在费用之上"怎么实现，需要特殊逻辑吗？

## A
**要点。** 不需要：TaxOnFees 是链上排在费用后面的一条规则，从 prior 里按 kind == "fee" 汇总。
**关键代码。** 
```python
fees = sum(l.amount for l in prior if l.kind == "fee")
return Decimal(fees) * self.bps / 10_000
```
**数字。** 10000 分、2.9% 加 30 分：费用 320，税 32，合计 352。
**易错。** 按规则名字猜种类，应该用 kind 字段。
