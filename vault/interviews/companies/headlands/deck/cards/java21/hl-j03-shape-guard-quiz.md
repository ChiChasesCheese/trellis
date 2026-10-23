---
id: hl-j03-shape-guard-quiz
node: java21.j03-pattern-switch
type: qa
step: 28
---
## Q
对 `sealed interface Shape permits Circle, Square, Tri`，只写 `case Circle`、`case Square when x > 0`、`case Tri`，`switch` 表达式能编译吗？

## A
**不能。** `case Square when x > 0` 带守卫，不算覆盖 `Square`，报 `does not cover all possible input values`（`x <= 0` 的 `Square` 没人处理）。

修法：再加一行无守卫的 `case Square`，或加 `default`。这也是"带守卫的分支不算覆盖"的标准陷阱。
