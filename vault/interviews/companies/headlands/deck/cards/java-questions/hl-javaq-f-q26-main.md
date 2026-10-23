---
id: hl-javaq-f-q26-main
node: java-questions.f-concurrency
type: qa
step: 4
---
## Q
`volatile` 保证什么、不保证什么？`volatile int count; count++` 线程安全吗？
What does `volatile` guarantee and what doesn't it? Is `volatile int count; count++` thread-safe?

## A
一句话：`volatile` 保证**可见性**（写立刻对后续读可见）和**有序性**（写前的操作不被重排到写后；读后的操作不被重排到读前），**不保证复合操作的原子性**；`count++` 是读-改-写三步，**不安全**。

- 适用：一个线程写、其他线程读的**状态标志**（`running`、`ready`）、安全发布不可变对象的引用、DCL 单例的引用。
- 不适用：计数器、"检查再行动"（check-then-act）。
- 交错过程：线程 1 读 5、线程 2 读 5，各自算 6 写回 6——两次加 1 只加了一次。
