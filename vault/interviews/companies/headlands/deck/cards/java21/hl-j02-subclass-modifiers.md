---
id: hl-j02-subclass-modifiers
node: java21.j02-sealed
type: qa
step: 4
---
## Q
`sealed` 类型的每个直接子类必须选哪三个修饰符之一？各自含义是什么，不写会怎样？

## A
| 修饰符 | 含义 |
|---|---|
| `final` | 到此为止，不能再有子类（最常见） |
| `sealed` | 继续封闭，自己也要 `permits` 一份名单 |
| `non-sealed` | 在这里重新开放，任何人都能继承 |

不写则编译错误 `sealed, non-sealed or final modifiers expected`。

**`record` 和 `enum` 隐式就是 `final`，不用写**。`non-sealed` 是 Java 里少见的带连字符的上下文关键字，不影响你把变量叫 `sealed`。
