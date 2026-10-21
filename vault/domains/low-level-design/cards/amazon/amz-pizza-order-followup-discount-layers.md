---
id: amz-pizza-order-followup-discount-layers
node: amazon.amz-pizza-order
type: qa
step: 6
tags: [grown]
---
## Q
在披萨订单里，面试官加「小号九折」和「三份里最便宜的一份免费」两条优惠，要改哪些类、不改哪些类？

## A
只新增规则类，不改 `Pizza`、`Order`、`PriceEngine`。

- 「小号九折」只看一份：`LineRule` 子类，`is_eligible` 判断尺寸，`apply` 在剩余价格上按基点算一次，半进位。
- 「三份里最便宜的免费」要看整单：`OrderRule` 子类，读行级折扣之后的各行结果。

```python
engine = PriceEngine(
    [PercentOff("小号九折", "10", frozenset({"S"}))],
    [CheapestFreePerN("买二送一", 3)],
)
```
引擎先逐行跑行级规则，再用折后结果跑整单规则。
