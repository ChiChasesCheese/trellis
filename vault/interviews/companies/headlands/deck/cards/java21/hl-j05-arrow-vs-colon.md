---
id: hl-j05-arrow-vs-colon
node: java21.j05-switch-expressions
type: qa
step: 5
---
## Q
`switch` 的箭头形式 `case X -> ...` 与冒号形式 `case X: ...` 在 fall-through、多标签、分支体、作用域上怎么比？能不能在同一个 `switch` 里混用？

## A
| | 箭头 `->` | 冒号 `:` |
|---|---|---|
| fall-through | **没有** | 有（要 `break`） |
| 多标签 | `case A, B ->` | `case A: case B:` 或 `case A, B:` |
| 分支体 | 一个表达式 / 一个块 / 一个 `throw` | 一串语句 |
| 作用域 | 每个分支自己一个 | 整个 `switch` 共享 |

**同一个 `switch` 里不能混用**，报 `different case kinds used in the switch`。推荐箭头形式，只有真的需要 fall-through 时才用冒号并写注释。
