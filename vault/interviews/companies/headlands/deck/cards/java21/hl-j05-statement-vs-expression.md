---
id: hl-j05-statement-vs-expression
node: java21.j05-switch-expressions
type: qa
step: 25
---
## Q
`switch` 语句和 `switch` 表达式在穷尽性和产出值上有什么区别？什么情况下 `switch` 语句也必须穷尽？

## A
- **语句**：`switch (x) { case 1 -> foo(); }`，对常量**不要求穷尽**，不产出值。
- **表达式**：`var y = switch (x) {...};`，**必须穷尽**，每个分支产出值或 `throw`。
- 语句若**用了模式或 `case null`**，也必须穷尽。
