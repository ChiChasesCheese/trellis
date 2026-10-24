---
id: pl-types-strong-weak-mechanism
node: types.strong-weak
type: qa
step: 4
---
## Q
Java 的数值运算是怎样做隐式转换的？为什么「加宽」转换也可能丢失精度，用 `int` 转 `float` 举例说明。

## A
Java 的二元数值提升（binary numeric promotion）规则分两步：

1. 先把 `byte`、`short`、`char` 提升为 `int`。
2. 再看两个操作数里「更宽」的那个：有 `double` 就都变 `double`；否则有 `float` 就都变 `float`；否则有 `long` 就都变 `long`；否则都是 `int`。

所以 `int + long` 的结果类型是 `long`，不用写转换。

加宽并不等于无损。`float` 只有 24 位有效的二进制位（尾数），而 `int` 有 32 位。2 的 24 次方是 16777216，超过它的整数 `float` 就无法逐个表示：

```java
int big = 16777217;      // 2^24 + 1
float f = big;           // 隐式加宽，合法，没有警告
System.out.println((int) f);   // 16777216
```

实际输出 `16777216`：赋值悄悄丢了 1。类似地，`long` 到 `double` 的加宽在超过 2 的 53 次方后也会丢精度。

这就是隐式转换的根本风险：转换在语言规范里「合法」，不等于数值不变。Rust 和 Go 干脆不提供这条路：你必须写出 `x as f32` 或 `float32(x)` 这样的转换，读代码的人一眼就能看到精度可能变化。
