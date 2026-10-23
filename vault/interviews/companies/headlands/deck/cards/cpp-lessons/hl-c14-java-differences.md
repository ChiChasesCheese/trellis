---
id: hl-c14-java-differences
node: cpp-lessons.c14-threads-mutex-cv
type: qa
step: 2
---
## Q
面试问：C++ 线程和 Java 线程在语义上的主要差别是什么？
Interview question: How do C++ threads differ from Java threads in semantics?

## A
- **数据竞争是 UB**（没有保底语义）。
- **`mutex` 不可重入**：对同一 `mutex` 重复加锁 → 死锁/UB。
- **没有 `interrupt`**：用 `stop_token`（C++20，协作式）。
- **没有 monitor**，也没有「守护线程」，没有虚拟线程。
- **线程对象析构时若仍可 join 会直接 `std::terminate`**。
