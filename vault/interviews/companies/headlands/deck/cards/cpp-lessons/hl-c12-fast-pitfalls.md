---
id: hl-c12-fast-pitfalls
node: cpp-lessons.c12-why-cpp-is-fast
type: qa
step: 14
---
## Q
谈「C++ 为什么快」时有哪五个常见的误区或坑？

## A
1. 说「C++ 因为编译所以快」：不完整，Go/Java 也编译。
2. 说「C++ 一定比 Java 快」：对非热点或 I/O 密集的程序差别很小；写得差的 C++（到处 `shared_ptr`、虚函数、`std::list`、`endl`）可能更慢。
3. 把「零开销抽象」理解成所有东西免费：`std::function`、异常抛出路径、`shared_ptr` 拷贝、iostream 都有代价。
4. **微基准**陷阱：被优化器整个删除、冷缓存、没预热、没有多次取中位数。
5. **不测量就优化**：先 profile（perf、Instruments、火焰图）。
