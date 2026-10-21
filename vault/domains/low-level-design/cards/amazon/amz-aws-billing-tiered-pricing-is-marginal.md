---
id: amz-aws-billing-tiered-pricing-is-marginal
node: amazon.amz-aws-billing
type: qa
step: 4
tags: [grown]
---
## Q
在 AWS 账单服务里，阶梯价应怎样计算？给一个具体输入和输出。

## A
每一档只对落在这一档内的那部分用量收这一档的价（边际，不是整体）：

```python
def charge(self, quantity):
    total, lower = Decimal(0), Decimal(0)
    for tier in self.tiers:
        upper = quantity if tier.up_to is None else min(quantity, tier.up_to)
        if upper > lower:
            total += (upper - lower) * tier.rate
            lower = upper
        if tier.up_to is None or quantity <= tier.up_to:
            break
    return total
```

前 51200 GB 每 GB 0.023、之后 0.022：102400 GB = 1177.60 + 1126.40 = 2304.00；整体解释会得 2252.80。
