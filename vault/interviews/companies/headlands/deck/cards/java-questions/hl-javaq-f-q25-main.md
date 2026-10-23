---
id: hl-javaq-f-q25-main
node: java-questions.f-concurrency
type: qa
step: 1
---
## Q
什么是 Java 内存模型（JMM）？"happens-before"是什么意思，为什么需要它？
What is the Java Memory Model? What does "happens-before" mean, and why do we need it?

## A
一句话：JMM 规定"一个线程的写在什么条件下**一定**对另一个线程的读可见、指令可以怎样重排"。**happens-before** 是核心：若 A happens-before B，则 A 的写对 B 可见且 A 不会被重排到 B 之后；**没有** happens-before 关系的读写就是**数据竞争**，结果不保证。

为什么需要：现代硬件和编译器为了快会**重排指令**、把变量缓存在**寄存器 / 核私有缓存**里。单线程里看不出来（保证"好像按顺序"），多线程就出问题。

两种坏结果（无同步时）：
- 线程 2 **永远看不到** `ready=true`（JIT 把读提到循环外，用寄存器里的旧值）。
- 看到 `ready=true` 但 `data` 还是 0（重排或缓存未刷新）。
