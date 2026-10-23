---
id: hl-j05-yield
node: java21.j05-switch-expressions
type: qa
step: 7
---
## Q
`yield` 是什么意思？它只能用在哪里？写一个块分支里用 `yield` 算交易时长的例子。

## A
`yield` 意为"**这个分支的结果是……，并结束整个 `switch` 表达式**"，类似方法里的 `return`，只能用在 `switch` 表达式的块里。

```java
case MON, TUE, WED, THU, FRI -> {
    int open = 9, close = 16;        // 块内局部变量，作用域只在这个分支
    yield close - open;
}
```
一个块里可以有多处 `yield`（例如 `if` 提前给值，末尾再给一次）。
