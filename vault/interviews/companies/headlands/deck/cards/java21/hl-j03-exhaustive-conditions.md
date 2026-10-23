---
id: hl-j03-exhaustive-conditions
node: java21.j03-pattern-switch
type: qa
step: 9
---
## Q
一组 `case` 对类型 `T` 穷尽，当且仅当满足哪些条件之一？

## A
满足任一条：
1. 有**无条件**模式（类型是 `T` 或其父类型，且无守卫），或有 `default`；
2. `T` 是 **sealed 接口 / 抽象 sealed 类**，且**每个**许可子类型都被覆盖（子类型自己 sealed 就递归展开）；
3. `T` 是 `enum` 且每个常量都有 `case`；
4. record 模式的情形按嵌套逐层展开（每层都要覆盖）。

对 `sealed` 层级写满子类型的无守卫 `case`，就不用 `default`。
