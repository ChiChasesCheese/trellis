---
id: hl-j04-destructuring-render
node: java21.j04-record-patterns
type: qa
step: 2
---
## Q
补全代码：用 record 模式把 `Answer`（`Value(Mean(var n, var d))` 或 `Empty()`）渲染成字符串：分母为 1 只打印分子，否则 `n/d`，空打印 `empty`。什么叫"解构"（destructuring）？

## A
```java
static String render(Answer a) {
    return switch (a) {
        case Value(Mean(var n, var d)) when d == 1 -> Long.toString(n);
        case Value(Mean(var n, var d)) -> n + "/" + d;
        case Empty() -> "empty";
    };
}
```
**解构**：数据的形状和使用它的代码长得一样——结构写进 `case`，字段自动取出，条件用 `when`。
