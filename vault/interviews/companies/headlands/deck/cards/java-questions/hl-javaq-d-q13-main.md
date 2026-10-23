---
id: hl-javaq-d-q13-main
node: java-questions.d-memory
type: qa
step: 10
---
## Q
一个 Java 对象占多少内存？对象头里有什么？`Integer`、两个字段的类、`int[10]` 各多大？
How much memory does a Java object take? What's in an object header? How big is `new Integer(5)`, a two-field class, an `int[10]`?

## A
一句话：64 位 HotSpot（压缩类指针）下，对象头 **12 字节**（8 字节 mark word + 4 字节类指针），数组再加 4 字节长度，头共 16；所有对象大小向 **8 字节对齐**。

- **mark word**：存哈希码、GC 年龄、锁状态。
- 空对象 **16**，`Integer` **16**，`int[10]` **56**（16 + 40）。
- 布局：普通对象 = 头 + 字段 + 填充；数组 = 头 + length + 元素 + 填充。
- JVM 可重排字段减少填充（大字段在前），不要依赖声明顺序。
