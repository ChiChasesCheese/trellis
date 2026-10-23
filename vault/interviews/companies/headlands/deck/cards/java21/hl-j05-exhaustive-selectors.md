---
id: hl-j05-exhaustive-selectors
node: java21.j05-switch-expressions
type: qa
step: 10
---
## Q
`switch` 表达式要穷尽，对 `enum`、`int` / `String`、`sealed` / 模式三类选择器分别怎样才算穷尽？

## A
| 选择器类型 | 怎样才算穷尽 |
|---|---|
| `enum` | 列全所有常量，或写 `default` |
| `int`、`char`、`String` 等 | **必须有 `default`**（值域是开放的） |
| `sealed` / 模式 | 覆盖所有许可子类型 |

漏一个枚举常量报 `the switch expression does not cover all possible input values`。
