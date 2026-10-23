---
id: hl-javaq-a-q02-follow-ups
node: java-questions.a-speed
type: qa
step: 8
---
## Q
被问到"Valhalla 想解决什么""Rust 也没有 GC，为什么不能说它就是更安全的 C++""今天的 Java 怎么得到连续内存布局"，各自的答案要点是什么？
What is Project Valhalla trying to fix? How do you get contiguous layout in Java today?

## A
- **Valhalla**：引入值类型（value class），消除对象头和指针，让对象能像 C++ struct 一样内联、连续排列。Java 21 **尚未发布**，只需知道动机，不要说已有。
- **Rust**：所有权（ownership）在**编译期**证明内存安全，没有 GC，边界检查可被优化掉；简答后转回 Java。
- **今天的 Java 怎么要连续布局**：用**原始类型数组**加并行数组（一个字段一个数组）；或用 `ByteBuffer` / `MemorySegment`（堆外内存段）把记录打包成字节布局，自己算偏移。
- 代价：失去对象语法的便利，要自己管理偏移与对齐。
