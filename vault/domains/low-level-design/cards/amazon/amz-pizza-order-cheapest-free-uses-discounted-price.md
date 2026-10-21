---
id: amz-pizza-order-cheapest-free-uses-discounted-price
node: amazon.amz-pizza-order
type: qa
step: 7
tags: [grown]
---
## Q
在披萨订单里，「每 2 份最便宜的一份免费」如果按原价免，会出什么错？给一个具体输入并说明修复。

## A
小号 800 分、中号 1000 分，小号先半价成 400 分。按原价免掉小号，减免是 800，总价 = 400 + 1000 − 800 = 600 分：这份小号只值 400，却被免掉 800，顾客多得 400。

修复：整单规则读行级折扣之后的每份均价（`final_cents // qty`），免的是 400，总价 1000 分。

```python
prices = sorted((r.final_cents // r.line.qty
                 for r in results for _ in range(r.line.qty)),
                reverse=True)
free = sum(prices[n - 1::n])   # 每满 n 份，组内最便宜的一份
```
