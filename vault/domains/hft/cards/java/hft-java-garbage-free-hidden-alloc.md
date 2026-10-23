---
id: hft-java-garbage-free-hidden-alloc
node: java.garbage-free
type: qa
step: 3
---
## Q
在热路径上，自动装箱、迭代器、捕获变量的 lambda、字符串拼接为什么会悄悄产生垃圾？怎么避免？

## A
这四处都在你没写 `new` 的地方分配了对象：
- **装箱**（boxing）：`Map<Long, Order>` 把 `long` 键包成 `Long` 对象，约 24 字节；改用原始类型 map，如 Agrona 的 `Long2ObjectHashMap`。
- **迭代器**：增强 for 遍历 `List` 会创建 `Iterator`；改用下标 for。
- **捕获变量的 lambda**：每次执行都创建一个捕获对象；改用字段、静态方法或显式传参。
- **字符串拼接**：`"id=" + id` 产生 `StringBuilder` 和 `String`；热路径不格式化日志，写预分配的缓冲区或异步记录。

逃逸分析有时能消掉其中一部分，但不保证，所以要实测。
