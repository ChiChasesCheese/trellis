---
id: cc-python-stdlib-decimal-calls
node: python.stdlib
type: qa
---
## Q
A rate of 2.9 % plus 30 cents must be applied to an amount and rounded half-up to the cent, exactly. Write the `decimal` calls — and name the one construction that is silently wrong.

## A
```python
from decimal import Decimal, ROUND_HALF_UP
rate = Decimal("0.029")                                   # from a STRING, always
fee  = (Decimal(amount) * rate).quantize(Decimal("1"), rounding=ROUND_HALF_UP) + 30
```

- `Decimal(0.029)` from a **float** inherits the float's binary error — it is the wrong construction.
- `quantize(exp, rounding=...)` is where rounding actually happens. Python's default is `ROUND_HALF_EVEN` (banker's), and the built-in `round()` on floats is half-even too — neither is the half-up most specs mean.
- With no library at all: `(amount * 29 + 500) // 1000` is exact half-up in one integer expression, and much faster inside a loop.

## Q zh
2.9% 的费率外加 30 分，必须精确地作用到金额上并按四舍五入（half-up）到分。写出 `decimal` 的调用 —— 并指出那个悄悄出错的构造方式。

## A zh
```python
from decimal import Decimal, ROUND_HALF_UP
rate = Decimal("0.029")                                   # 永远从字符串构造
fee  = (Decimal(amount) * rate).quantize(Decimal("1"), rounding=ROUND_HALF_UP) + 30
```

- 从**浮点数**构造的 `Decimal(0.029)` 会继承浮点的二进制误差 —— 那就是错的构造方式。
- 舍入真正发生在 `quantize(exp, rounding=...)`。Python 的默认是 `ROUND_HALF_EVEN`（银行家舍入），内置 `round()` 对浮点也是 half-even —— 都不是多数题面说的 half-up。
- 完全不用库：`(amount * 29 + 500) // 1000` 是一个整数表达式里的精确 half-up，在循环里还快得多。
