---
id: hl-j03-guard-not-cover
node: java21.j03-pattern-switch
type: qa
step: 10
---
## Q
下面对 `Object` 的 `switch` 为什么不穷尽？带守卫的分支算不算覆盖？

```java
case String s when s.length() > 3 -> "long";
case Integer i -> "int";
```

## A
带守卫的分支**不算覆盖**：守卫可能为假，编译器不能假定它覆盖了该类型。

这里 `String` 且长度 ≤ 3 的情形没人处理，对 `Object` 选择器也没有 `default` 或无条件模式，所以编译错误（`does not cover all possible input values`）。

修法：再加一行无守卫的 `case String s`，或加 `default`。
