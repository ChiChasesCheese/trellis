---
id: cc-rules-round-floor-vs-truncate
node: rules.rounding
type: qa
---
## Q
`//` and `int()` both "round down". Where do they disagree, and which one does a spec that says "truncate" mean?

## A
**They disagree on negatives: `-7 // 2` is `-4` (floor, toward minus infinity), `int(-7 / 2)` is `-3` (truncate, toward zero).**

"Truncate" in a fee statement — "433.64 is withheld as 433" — means toward zero, which for the non-negative amounts these rules describe is the same as floor. The moment a negative appears (a refund, a credit note, a negative adjustment) the two diverge by one unit.

Decide by asking whether the quantity can be negative. If it can, write the mode explicitly (`math.floor`, `int()`, or `Decimal` with `ROUND_FLOOR`/`ROUND_DOWN`) rather than letting `//` decide for you.

## Q zh
`//` 和 `int()` 都"向下取整"。它们在哪里不一致？题面说「截断」时指的是哪一个？

## A zh
**它们在负数上不一致：`-7 // 2` 是 `-4`（floor，向负无穷），`int(-7 / 2)` 是 `-3`（truncate，向零）。**

手续费题面里的「截断」 —— 「433.64 按 433 扣留」 —— 指的是向零取整；对这些规则所描述的非负金额而言，它与 floor 相同。一旦出现负数（退款、贷记单、负向调整），两者就相差一个单位。

判断办法是问这个量能否为负。如果能，就显式写出模式（`math.floor`、`int()`，或带 `ROUND_FLOOR`/`ROUND_DOWN` 的 `Decimal`），而不是让 `//` 替你决定。
