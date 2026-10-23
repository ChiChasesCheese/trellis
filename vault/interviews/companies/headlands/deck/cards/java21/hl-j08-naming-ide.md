---
id: hl-j08-naming-ide
node: java21.j08-var
type: qa
step: 21
---
## Q
用了 `var` 之后变量命名要怎么补偿？"IDE 会显示推导类型"为什么不是理由？

## A
- **命名要补偿类型信息**：变量名要多承担"这是什么"，`var results`、`var idToOrder` 比 `var r`、`var m` 好得多。
- **不要为"少打几个字"破坏可读性**：IDE 能显示推导类型，但**代码评审、GitHub diff、日志片段**没有 IDE。代码是写给人读的。
