---
id: hl-j02-vs-enum-interface
node: java21.j02-sealed
type: qa
step: 2
---
## Q
开放 `interface`、`enum`、`sealed interface` + `record` 三者在"有几种、能否带不同字段、能否多实例、能否检查 switch 穷尽"上怎么比？

## A
| | 开放 interface | enum | sealed interface + record |
|---|---|---|---|
| 有哪几种 | 谁都能加 | 固定 | 固定（`permits` 列出） |
| 每种带不同字段 | 能 | 不能（字段都一样） | 能 |
| 每种多个实例 | 能 | 不能（每个常量一个） | 能 |
| 编译器检查 switch 穷尽 | 不能 | 能 | 能 |

`sealed` 就是"像 enum 一样封闭，又像类一样各带字段"。
