---
id: craft-round-once-at-the-boundary-2-rounding-modes
node: craft.idioms.round-once-at-the-boundary
type: qa
step: 2
---
## Q
**在边界处取整一次 · 银行家舍入和四舍五入差在哪，内置 `round()` 能不能用来算钱**｜写法

计费引擎的取整用 `ROUND_HALF_EVEN`，折扣引擎用 `ROUND_HALF_UP`。两者在 2.5、3.5 上结果不同吗？为什么大量求和时银行家舍入的偏差更小？金额代码里为什么不直接用 `round()`？

## A
**要点。** `ROUND_HALF_UP`：恰好在中间的数（.5）总是进位。`ROUND_HALF_EVEN`（银行家舍入，banker's rounding）：.5 取最近的**偶数**，2.5 → 2，3.5 → 4。一半进、一半舍，对大量恰好是 .5 的数求和，高低互相抵消，不像 HALF_UP 一路偏高。Python 的 `round()` 对整数和 float 都是银行家舍入；`Decimal.quantize` 不带 `rounding=` 时用的是上下文的默认值（`ROUND_HALF_EVEN`），所以要显式写出来，让读代码的人知道意图。

```python
vals = ["0.5", "1.5", "2.5", "3.5"]
print("值        ", vals)
print("HALF_UP   ", [int(Decimal(v).quantize(Decimal(1), rounding=ROUND_HALF_UP)) for v in vals])
print("HALF_EVEN ", [int(Decimal(v).quantize(Decimal(1), rounding=ROUND_HALF_EVEN)) for v in vals])
print("内置 round", [round(float(v)) for v in vals])  # 也是银行家舍入

# 偏差：把大量恰好 .5 的数各取整再求和
xs = [Decimal(n) + Decimal("0.5") for n in range(1000)]
exact = sum(xs)
up = sum(x.quantize(Decimal(1), rounding=ROUND_HALF_UP) for x in xs)
even = sum(x.quantize(Decimal(1), rounding=ROUND_HALF_EVEN) for x in xs)
print("1000 个 .5 求和, 精确值", exact)
print("HALF_UP   偏高", up - exact)
print("HALF_EVEN 偏差", even - exact)

# round() 对 float 的陷阱：2.675 在二进制里略小于 2.675
print("round(2.675, 2) =", round(2.675, 2))
print("Decimal 字符串 HALF_UP:", Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
```

实际输出：

```
值         ['0.5', '1.5', '2.5', '3.5']
HALF_UP    [1, 2, 3, 4]
HALF_EVEN  [0, 2, 2, 4]
内置 round [0, 2, 2, 4]
1000 个 .5 求和, 精确值 500000.0
HALF_UP   偏高 500.0
HALF_EVEN 偏差 0.0
round(2.675, 2) = 2.67
Decimal 字符串 HALF_UP: 2.68
```

**为什么不用 `round()` 算钱。** 它作用于 float：`round(2.675, 2)` 得到 `2.67`，因为 2.675 在二进制里略小于 2.675。float 一进入，误差在取整之前就已产生。金额要么用 `Decimal` 显式取整，要么用整数运算（见下一张卡）。

**易错。** 选哪种舍入是业务规则，不是代码风格：税务、账单、行业规范常常指定了一种。选定后写进文档，所有取整点用同一个。
