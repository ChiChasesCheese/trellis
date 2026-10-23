---
id: hl-j06-total-pattern
node: java21.j06-instanceof-pattern
type: qa
step: 10
---
## Q
Java 21 对 `instanceof` 模式放开了什么？`String s; s instanceof String t` 在 Java 16–20 和 21 里分别怎样，语义是什么？

## A
Java 21 允许"**总是匹配**"的模式：`String s; s instanceof String t`。

- Java 16–20：编译错误。
- Java 21：合法，语义是"**`s` 非 `null` 时为 `true`**"。

放开是为了与 `switch` 的无条件模式规则统一。
