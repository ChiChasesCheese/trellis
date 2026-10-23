---
id: hl-j02-exhaustive-switch
node: java21.j02-sealed
type: qa
step: 13
---
## Q
`sealed` 对 `switch` 穷尽检查（exhaustiveness）有什么影响？它的"真正价值"是什么？漏一个分支时报什么错？

## A
`javac` 检查 `switch` 是否穷尽时，会从 sealed 类型出发**递归展开 `PermittedSubclasses`**：有 `case Ok` 和 `case Err` 就知道没有第三种，**不需要 `default`**。漏一种就是编译错误：

```
error: the switch expression does not cover all possible input values
```
真正价值：让"**新增一个变体**"变成一个**编译期事件**——把 `permits` 加一项，所有没处理它的 `switch` 当场报错，而不是线上炸。
