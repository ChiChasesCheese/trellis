---
id: hl-j03-exhaustive-rule
node: java21.j03-pattern-switch
type: qa
step: 8
---
## Q
哪些 `switch` 必须穷尽（exhaustive）？没穷尽时的编译错误是什么？哪种 `switch` 例外？

## A
- **`switch` 表达式**（`return switch ...` / `var x = switch ...`）必须覆盖选择器类型的所有可能值，否则编译错误：`the switch expression does not cover all possible input values`。
- **用了模式或 `case null` 的 `switch` 语句**也必须穷尽：`the switch statement does not cover all possible input values`。
- **例外**：只有"老式"`switch` 语句（`int` / `String` / `enum` 常量分支，无模式无 null）可以不穷尽。

穷尽性是模式匹配 `switch` 最重要的一条。
