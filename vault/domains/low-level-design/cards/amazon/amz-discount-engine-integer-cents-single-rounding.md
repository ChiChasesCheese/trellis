---
id: amz-discount-engine-integer-cents-single-rounding
node: amazon.amz-discount-engine
type: qa
step: 4
tags: [grown]
---
## Q
在购物车折扣引擎里，金额和折扣比例分别用什么表示？舍入发生在哪里、怎么做？

## A
金额用整数分，比例用整数基点（万分之一，8.5% 记 850）。舍入只在每条折扣的 `apply` 里发生一次，用纯整数的半进位除法。

```python
def div_half_up(numerator: int, denominator: int) -> int:
    return (2 * numerator + denominator) // (2 * denominator)

div_half_up(199 * 850, 10_000)   # 16.915 分 -> 17
div_half_up(105 * 850, 10_000)   # 8.925 分 -> 9
```

字符串价格先经 `Decimal` 精确转成分，不经过 `float`。
