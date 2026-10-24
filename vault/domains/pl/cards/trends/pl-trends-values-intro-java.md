---
id: pl-trends-values-intro-java
node: trends.value-types
type: qa
step: 3
---
## Q
Java 的对象为什么都带“身份”与对象头？`Integer[]` 与 `int[]` 的区别，以及 Valhalla 项目的值类（value class）想改变什么？

## A
**Java 的对象模型**：除了八种基本类型（`int`、`double` 等），所有东西都是堆上的对象，通过引用访问。每个对象有一个**对象头**（常见约 12 字节，存类型指针和同步/哈希用的标记），并且有**身份**（identity）：两个内容相同的对象依然是两个对象，`==` 比较引用。

**数组的差别**：
- `int[]`：连续的 4 字节整数，没有对象头，遍历最快。
- `Integer[]` 或 `List<Integer>`：连续的是**引用**，每个元素是堆上一个单独的 `Integer` 对象（约 16 字节）。`record P(int x, int y, int z)` 的数组也是引用数组，每个 `P` 约 24 字节（头加三个整数）。

**一次本机测量**：一千万个元素，按乱序下标读取 `x`，`P[]`（对象数组）约 55 ms，把 `x` 单独存成 `int[]` 约 13 ms，约 4 倍。顺序读取时两者接近（约 3 ms 对 2 ms），因为对象按分配顺序碰巧相邻；一旦对象在内存里被打乱，每次访问都是缓存未命中。

**Valhalla 想做什么**：引入**值类**（value class），声明放弃身份：

```java
value class Point { int x; int y; ... }
```

放弃身份后，JVM 可以把 `Point[]` 摊平成连续的 x、y 数据，不要对象头，像 `int[]` 一样快；`==` 比较字段而不是引用。代价是失去 `synchronized`、身份哈希等依赖身份的功能。这个特性仍在孵化，本机 Java 25 的编译器不接受 `value class` 语法（真实报错 `<identifier> expected`）。

**要记住的一点**：Java 的“一切皆引用对象”是 1995 年为简单与安全做的选择，布局控制是 Valhalla 要补回来的能力。
