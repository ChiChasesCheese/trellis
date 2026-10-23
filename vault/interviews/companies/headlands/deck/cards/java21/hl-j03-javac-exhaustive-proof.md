---
id: hl-j03-javac-exhaustive-proof
node: java21.j03-pattern-switch
type: qa
step: 19
---
## Q
`javac` 是怎么证明一个 `sealed` 层级的 `switch` 穷尽的？检查发生在编译期还是运行时？

## A
编译器把所有**无守卫**的 `case` 模式收集起来，对选择器类型做**递归覆盖检查**：
- `Result`（`sealed`）展开成 `Ok`、`Err`（读 `PermittedSubclasses`）；
- 每个子类型在 `case` 里有无守卫的类型模式就算覆盖；
- 子类型自己 `sealed` 就再展开；
- 全覆盖即穷尽，否则报 `does not cover all possible input values`。

检查全在**编译期**，运行时只多一个永远走不到的 `MatchException` 分支。
