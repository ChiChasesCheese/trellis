---
id: craft-round-once-at-the-boundary-1-one-rounding-point
node: craft.idioms.round-once-at-the-boundary
type: qa
step: 1
---
## Q
**在边界处取整一次 · 为什么全系统只留一个 `_to_minor`**｜写法

账单有三行商品，每行 1.10 元，税率 8.5%。每一行算税、各自四舍五入到分、最后相加，和「先把三行的税精确相加、最后取整」，结果一样吗？计费引擎为什么坚持只有一个取整的地方？

## A
**要点。** 不一样。取整是丢信息的操作，每取整一次就丢一点，多次取整的误差会累计。做法是中间值保持全精度（`Decimal` 或 `Fraction`，不取整），只在**要交出去的那一刻**（写进账单、存进账本、返回给调用方）取整一次，并且全系统只有一个函数做这件事。

```python
def to_minor(x: Decimal) -> int:
    """全系统唯一的取整点。"""
    return int(x.quantize(Decimal(1), rounding=ROUND_HALF_EVEN))

TAX_BPS = 850                       # 8.5%
lines = [110, 110, 110]             # 三行商品，单位：分

def tax(amount_cents: int) -> Decimal:
    return Decimal(amount_cents) * TAX_BPS / 10_000      # 全精度，不取整

per_line = sum(to_minor(tax(a)) for a in lines)           # 每行各取整一次再相加
once = to_minor(sum((tax(a) for a in lines), Decimal(0)))  # 全精度相加，最后取整一次
print("每行税(精确):", [str(tax(a)) for a in lines])
print("每行取整再相加:", per_line, "分")
print("相加后取整一次:", once, "分")
```

实际输出：

```
每行税(精确): ['9.35', '9.35', '9.35']
每行取整再相加: 27 分
相加后取整一次: 28 分
```

**为什么。** 单一取整点还有第二个好处：规则变了（银行家舍入改成 `HALF_UP`）只改一处。取整散落在每条规则里，换规则要改很多处，漏掉一处就是「有的行按旧规则、有的按新规则」，对账永远对不平，而且没人能一眼看出来。

**代价。** 「一行只取整一次」是指账单的一行，而不是整张账单只取整一次：账单每一行最终都要有整数分的金额，总额等于各行之和。所以取整点是「每一行产出时」，不是「每一步计算时」。
