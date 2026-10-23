---
id: hl-j05-result-type
node: java21.j05-switch-expressions
type: qa
step: 12
---
## Q
`switch` 表达式的结果类型怎么确定？在赋值上下文和独立位置（`var x = switch ...`）各怎样？分支是 `int`、`double`、`long` 时结果是什么？

## A
- **赋值上下文**（`String s = switch ...`）：每个分支都得能赋给 `String`，否则 `bad type in switch expression`。
- **独立位置**（`var x = switch ...`）：取各分支的**公共类型**，数值分支做数值提升。
- 分支是 `int`、`double`、`long` 时结果提升为 **`double`**，例如分支值依次为 `1`（int）、`2.5`（double）、`3`（long）时，输出 `1.0 2.5 3.0`。

`long` 变 `double` 会丢精度，各分支类型一致最安全。`Integer` 与 `int` 混用会拆箱，其中一个为 `null` 时 NPE。
