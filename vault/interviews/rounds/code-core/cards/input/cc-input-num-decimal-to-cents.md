---
id: cc-input-num-decimal-to-cents
node: input.numbers
type: qa
---
## Q
Amounts arrive as decimal strings with up to two places: `12.34`, `7`, `0.5`. Convert them to integer cents exactly.

## A
**Convert through `Decimal`, or split the string — never through `float`.**

```python
from decimal import Decimal, ROUND_HALF_UP
cents = int(Decimal(s).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) * 100)
```

`Decimal(s)` takes the *string*, so `0.1` is exactly one tenth; `Decimal(0.1)` from a float is not. `int(float(s) * 100)` truncates `7.35` to `734` on some values, which is a wrong cent that only shows up in one hidden test. `7` becomes 700 and `0.5` becomes 50 — pad, do not assume two digits. See [[cc-rules-money-integer-minor-units]].

## Q zh
金额以最多两位小数的字符串到达：`12.34`、`7`、`0.5`。把它们精确转成整数分。

## A zh
**走 `Decimal`，或者直接切字符串 —— 绝不经过 `float`。**

```python
from decimal import Decimal, ROUND_HALF_UP
cents = int(Decimal(s).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP) * 100)
```

`Decimal(s)` 接收的是**字符串**，所以 `0.1` 恰好是十分之一；而由 float 构造的 `Decimal(0.1)` 不是。`int(float(s) * 100)` 在某些值上会把 `7.35` 截成 `734`，这一分钱的偏差只会在某个隐藏测试里冒出来。`7` 要变 700、`0.5` 要变 50 —— 补齐位数，别假设一定有两位。见 [[cc-rules-money-integer-minor-units]]。
