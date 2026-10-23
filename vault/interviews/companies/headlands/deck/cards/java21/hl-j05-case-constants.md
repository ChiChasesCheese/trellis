---
id: hl-j05-case-constants
node: java21.j05-switch-expressions
type: qa
step: 24
---
## Q
`case` 标签对表达式有什么要求？`case x ->`（`x` 是普通变量）、重复常量会怎样？

## A
`case` 的表达式必须是**编译期常量**：
- `case x ->`（`x` 是普通变量）不行；
- `case MAX ->` 要求 `MAX` 是 `static final` 的编译期常量；
- 重复常量报 `duplicate case label`。

`default` 的位置：老 `switch` 里 `default` 放中间有 fall-through 含义；箭头形式没这问题，但仍建议放最后。
