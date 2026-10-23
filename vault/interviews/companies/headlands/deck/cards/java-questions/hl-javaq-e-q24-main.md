---
id: hl-javaq-e-q24-main
node: java-questions.e-jit-gc
type: qa
step: 23
---
## Q
除了 GC，JVM 还有什么会让进程暂停？什么是 safepoint？
Besides GC, what else makes a JVM pause? What's a safepoint?

## A
一句话：**safepoint** 是所有 Java 线程都停在已知安全位置的时刻，JVM 在其中做 GC、去优化、类重定义、线程转储等操作；等所有线程到达的时间（time-to-safepoint）和 safepoint 里的工作都算暂停。

GC 之外的抖动成因：
- 页错误 / 内存回收；
- OS 调度与 CPU 争用（含 JIT 编译线程）；
- 类加载；
- 日志与 I/O。
