---
id: hl-c13-cpp-vs-jmm
node: cpp-lessons.c13-memory-model-atomics
type: qa
step: 1
---
## Q
C++ 内存模型和 Java 内存模型（JMM）怎么对应？C++ 的 `volatile` 能用来做线程同步吗？

## A
- JMM 用 `volatile`、`synchronized`、`final` 定义可见性和有序性（happens-before）；`java.util.concurrent.atomic` 提供 CAS。
- C++11 起有同样严格的内存模型：`std::atomic<T>` 的每个操作可以指定 `memory_order`，默认 `seq_cst` 最强（类似 Java `volatile` 的语义），可按需放松换性能。Java 的 VarHandle 提供 acquire/release 模式，C++ 把这些做成每次操作的参数。
- **C++ 的 `volatile` 不是线程同步工具**：它只阻止编译器优化掉访问，不要用它代替 `atomic`。
