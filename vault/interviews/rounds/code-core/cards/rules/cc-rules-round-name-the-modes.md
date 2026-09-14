---
id: cc-rules-round-name-the-modes
node: rules.rounding
type: qa
---
## Q
Name the four rounding modes a money rule can ask for, and what each does to `2.5`, `-2.5` and `2.4`.

## A
**Half-up · half-even (banker's) · floor · truncate.**

```
                2.5    -2.5    2.4
ROUND_HALF_UP     3      -3      2     ties away from zero
ROUND_HALF_EVEN   2      -2      2     ties to even (Python's round, Decimal default)
ROUND_FLOOR       2      -3      2     toward minus infinity  (Python //)
ROUND_DOWN        2      -2      2     toward zero            (int())
```

Floor and truncate agree on positives and disagree on negatives, which is why a fee rule that never sees a negative amount can hide the difference until a refund arrives. Read the statement's verb — "rounded", "rounded down", "truncated" — and name the mode in the code.

## Q zh
说出货币规则可能要求的四种取整模式，以及它们对 `2.5`、`-2.5`、`2.4` 各自的结果。

## A zh
**half-up · half-even（银行家）· floor · truncate。**

```
                2.5    -2.5    2.4
ROUND_HALF_UP     3      -3      2     ties away from zero
ROUND_HALF_EVEN   2      -2      2     ties to even (Python's round, Decimal default)
ROUND_FLOOR       2      -3      2     toward minus infinity  (Python //)
ROUND_DOWN        2      -2      2     toward zero            (int())
```

floor 与 truncate 在正数上一致、在负数上不一致，所以一条从没见过负金额的手续费规则可以把差别藏到某笔退款到来为止。读清题面的动词 —— 「四舍五入」「向下取整」「截断」 —— 并在代码里写出模式名。
