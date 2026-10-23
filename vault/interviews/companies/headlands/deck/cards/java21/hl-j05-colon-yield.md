---
id: hl-j05-colon-yield
node: java21.j05-switch-expressions
type: qa
step: 8
---
## Q
冒号形式的 `switch` 表达式怎么给值？写出把 1 映射为 `"one"`、2 或 3 映射为 `"two or three"`、其余为 `"many"` 的版本。`yield` 是关键字吗？

## A
冒号形式的 `switch` 表达式**也要用 `yield`**：

```java
return switch (n) {
    case 1:
        yield "one";
    case 2:
    case 3:
        yield "two or three";
    default:
        yield "many";
};
```
`yield` 是**上下文关键字**：老代码里叫 `yield` 的变量 / 方法名通常还能用，但调用叫 `yield` 的方法要写 `this.yield(...)` 或 `Thread.yield()`。
