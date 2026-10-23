---
id: hft-java-object-layout-header
node: java.object-layout
type: qa
step: 1
---
## Q
一个 Java 对象在内存里除了你声明的字段，还带着什么？这对内存占用有什么影响？

## A
每个对象前面都有**对象头**（object header）：一个 mark word（存哈希码、锁状态、GC 年龄等）加一个类指针（指向类的元数据）。64 位 HotSpot 开启压缩指针时对象头约 12 字节，对象总大小再向上对齐到 8 的倍数。

例：`record Fill(long id, long px, int qty)` 有 8 + 8 + 4 = 20 字节的真实数据，加 12 字节对象头，正好 32 字节，头部开销占三分之一以上。如果用 100 万个这样的对象，光是对象头就浪费约 12 MB，而且数组里还要另存 100 万个引用。

这就是低延迟代码常常用原始类型数组、而不是对象集合的原因之一。
