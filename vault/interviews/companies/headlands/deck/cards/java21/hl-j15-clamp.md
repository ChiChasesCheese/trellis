---
id: hl-j15-clamp
node: java21.j15-math-string-utils
type: qa
step: 7
---
## Q
Java 21 的 `Math.clamp` 怎么用？有哪四个重载？`min > max` 时会怎样，相比手写 `Math.max(lo, Math.min(hi, v))` 好在哪？

## A
```java
Math.clamp(150, 0, 100)             // 100
Math.clamp(-5, 0, 100)              // 0
int shift = Math.clamp(40L, 0, 32); // (long value, int min, int max) 返回 int
Math.clamp(3.7, 0.0, 1.0)           // 1.0
```
四个重载：`(long, int, int) -> int`、`(long, long, long) -> long`、`(double, double, double)`、`(float, float, float)`。

`min > max` 抛 `IllegalArgumentException`；手写的 `Math.max(lo, Math.min(hi, v))` 在 `lo > hi` 时**悄悄返回 `lo`**，掩盖参数写反的 bug。
