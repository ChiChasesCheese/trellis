---
id: hl-j04-point-instanceof
node: java21.j04-record-patterns
type: qa
step: 16
---
## Q
补全代码：`Object o = new Point(3, 4);`，用 `instanceof` 的 record 模式求 `x*x + y*y`；`"hello" instanceof Point(var x, var y)` 的结果是什么？

## A
```java
record Point(long x, long y) {}
Object o = new Point(3, 4);
if (o instanceof Point(long x, long y)) {
    System.out.println("distance^2 = " + (x * x + y * y));    // 25
}
if (o instanceof Point(var x, var y) && x < y) { ... }          // 可接 &&
```
`"hello" instanceof Point(var x, var y)` 是 **`false`**：类型不对，整个条件为假，不抛异常。
