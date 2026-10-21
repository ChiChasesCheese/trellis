---
id: amz-aws-billing-stage1-invoice-in-code
node: amazon.amz-aws-billing
type: qa
step: 3
tags: [grown]
---
## Q
在 AWS 账单服务里，第 1 关（用量乘费率、汇总成账单）的核心方法怎么写？

## A
按 (服务, 指标) 把用量加起来，对每个 key 调一次费率再舍入，总额是各行之和：

```python
def invoice(self, start, end):
    totals = defaultdict(Decimal)
    for rec in self.ledger.between(start, end):
        totals[(rec.service, rec.metric)] += rec.quantity
    lines = tuple(
        InvoiceLine(s, m, q, Money.from_decimal(self.plans[(s, m)].charge(q)))
        for (s, m), q in sorted(totals.items())
    )
    return Invoice(lines)
```

费率只在最后舍入一次；下一关新增费率类时，这个方法不用改。
