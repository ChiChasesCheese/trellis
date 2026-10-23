---
id: hft-java-object-layout-jol
node: java.object-layout
type: qa
step: 4
---
## Q
JOL（Java Object Layout）是什么工具？用它看对象布局时，通常想确认什么？

## A
JOL 是 OpenJDK 提供的小工具库，能打印一个类的实例在内存中的真实布局：对象头大小、每个字段的偏移量、字段之间的填充（padding）、对象总大小。用法如 `ClassLayout.parseClass(Order.class).toPrintable()`。

用它主要确认四件事：
- 对象实际多大（头 + 字段 + 对齐），而不是凭感觉；
- 字段是否被 JVM 重排（HotSpot 会按大小重排字段以减少填充，不一定按声明顺序）；
- 一起被读的热字段是否落在同一条 64 字节缓存行；
- `byte`、`int`、`long` 混排是否产生了空洞。

用布局数据决定要不要拆字段、换数组，而不是靠猜。
