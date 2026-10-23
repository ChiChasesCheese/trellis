---
id: hl-j05-no-escape
node: java21.j05-switch-expressions
type: qa
step: 9
---
## Q
`switch` 表达式的分支里能不能写 `break`、`return`、`continue`？为什么？允许的出口有哪些？

## A
**都不能**，因为表达式必须产出值，这些跳转会让控制流跳出而没有值：
- `break;` → `attempt to break out of a switch expression`
- `return 5;` → `attempt to return out of a switch expression`
- `continue;` → 同理

允许的出口只有：**`yield`、`throw`、箭头表达式**。
