---
id: hl-j13-shared-case
node: java21.j13-unnamed-variables
type: qa
step: 8
---
## Q
`case A a, B b ->` 为什么非法，`case A _, B _ ->` 为什么合法？

## A
`case A a, B b ->` 里 `a`、`b` 在分支体都要可用，但每次只有一个模式匹配，另一个未初始化，编译器无法保证安全，报错 `illegal fall-through from a pattern`。

**所有模式都不引入变量（全是 `_`）时没有这个问题，所以允许**：

```java
case Cancel _, Reject _ -> "TERMINAL";
```
`sealed` 穷尽性照常：`Cancel _, Reject _` 仍分别算覆盖这两个子类型。也可以改用共同父接口的变量。
