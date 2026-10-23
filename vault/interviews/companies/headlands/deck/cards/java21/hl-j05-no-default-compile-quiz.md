---
id: hl-j05-no-default-compile-quiz
node: java21.j05-switch-expressions
type: qa
step: 29
---
## Q
把 "`SELL` / `SHORT` 返回 -1，`BUY` 返回 1" 写成不带 `default` 也能编译的 `switch` 表达式，需要 `Side` 具备什么条件？

## A
```java
int s = switch (side) { case BUY -> 1; case SELL, SHORT -> -1; };
```
条件：`Side` 是 `enum`，且这里**列全了所有常量**（`BUY`、`SELL`、`SHORT`）。编译器认为已穷尽，不需要 `default`。

如果 `Side` 是 `int` 或 `String` 之类开放集合，就必须有 `default`。
