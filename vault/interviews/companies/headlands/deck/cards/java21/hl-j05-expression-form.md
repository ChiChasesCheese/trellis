---
id: hl-j05-expression-form
node: java21.j05-switch-expressions
type: qa
step: 4
---
## Q
补全代码：用 `switch` 表达式写 `sign(Side s)`，`BUY` 返回 1，`SELL` 和 `SHORT` 返回 -1。它相比老写法有哪四点改变？

## A
```java
static int sign(Side s) {
    return switch (s) {
        case BUY -> 1;
        case SELL, SHORT -> -1;
    };
}
```
四点：
1. `switch` 是**表达式**：有值，能 `return`、赋值、当参数；
2. 箭头 `->` **没有 fall-through**，只执行箭头右边；
3. 多标签用**逗号** `case SELL, SHORT`；
4. `enum` 列全常量就**不需要 `default`**，漏了编译错误。
