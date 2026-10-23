---
id: hl-j04-subpattern-kinds
node: java21.j04-record-patterns
type: qa
step: 5
---
## Q
record 模式里的子模式可以是哪四种？各举一个例子。

## A
| 子模式 | 例子 | 含义 |
|---|---|---|
| 类型模式（显式类型） | `Point(long x, long y)` | 组件类型必须兼容 |
| `var` 模式 | `Point(var x, var y)` | 类型由编译器推导为组件的声明类型 |
| 嵌套 record 模式 | `Value(Mean(var n, var d))` | 再拆一层 |
| 零组件 record | `Empty()` | 括号里什么都没有 |

`var` 最省心：编译器知道每个组件的类型，`var` 照抄；需要明确意图时才写显式类型。
