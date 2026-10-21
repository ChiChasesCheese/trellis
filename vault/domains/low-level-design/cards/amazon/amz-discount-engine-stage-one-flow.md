---
id: amz-discount-engine-stage-one-flow
node: amazon.amz-discount-engine
type: qa
step: 3
tags: [grown]
---
## Q
在 Amazon 购物车折扣引擎里，对一行商品依次应用多个行级折扣的核心循环怎么写？

## A
先用 `is_eligible` 筛选，再逐个 `apply`；每个折扣看到的是前面减完后的剩余价格，减免不得超过剩余价格。

```python
def price_line(line, discounts):
    remaining = line.unit_cents * line.qty
    adjustments = []
    for d in discounts:
        if not d.is_eligible(line):
            continue
        amount = min(d.apply(line, remaining), remaining)
        if amount > 0:
            adjustments.append((d.label, amount))
            remaining -= amount
    return adjustments, remaining
```
