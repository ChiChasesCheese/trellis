---
id: hl-j04-render-instanceof
node: java21.j04-record-patterns
type: qa
step: 26
---
## Q
补全代码：不用 `switch`，只用 `instanceof` 的 record 模式把 `Answer` 渲染成字符串（`Value(Mean(n,d))`：`d==1` 打印 `n`，否则 `n/d`；`Empty` 打印 `empty`）。

## A
```java
static String render(Answer a) {
    if (a instanceof Value(Mean(var n, var d))) {
        return d == 1 ? Long.toString(n) : n + "/" + d;
    }
    if (a instanceof Empty) return "empty";
    throw new IllegalArgumentException();
}
```
`instanceof` 版不会做穷尽检查，所以末尾仍要人工兜底；`switch` 版配合 `sealed` 才有编译器帮你检查。
