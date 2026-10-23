---
id: hl-cq-q30-volatile-data-race
node: cpp-questions.g-concurrency
type: qa
step: 13
---
## Q
面试题：C++ 的 `volatile` 线程安全吗？什么是数据竞争？
Is `volatile` thread-safe in C++? What is a data race?

## A
- **不是。** C++ 的 `volatile` 只告诉编译器“每次访问都要真读写、别优化掉”，**不提供原子性，也不提供线程间顺序**（Java 的 `volatile` 才有）。
- **数据竞争**：两个线程同时访问同一位置、至少一个是写、且没有同步。它是**未定义行为**，即使看起来“无害”。
- `volatile` 只留给内存映射的硬件寄存器。
