---
id: amz-pizza-order-menu-as-data-price-by-size
node: amazon.amz-pizza-order
type: qa
step: 4
tags: [grown]
---
## Q
在披萨订单里，配料价格随尺寸变，怎么存才能做到「新增一种配料只加一行数据」？举一个输入和输出。

## A
每种配料存一张「尺寸 → 价格（分）」的小表，价格 = 基础价 + 饼底加价 + 该尺寸下每种配料的价，全是字典查找，每份披萨 O(配料数)。

```python
toppings["pepperoni"] = ToppingSpec({"S": 150, "M": 200, "L": 250})
# 大号厚饼底 + pepperoni + mushroom：
# 1200 + 100 + 250 + 150 = 1700 分
```
同样的 pepperoni 放在小号是 150，所以价格不能是「每种配料一个数字」。
