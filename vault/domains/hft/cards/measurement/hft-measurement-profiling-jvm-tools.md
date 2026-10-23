---
id: hft-measurement-profiling-jvm-tools
node: measurement.profiling
type: qa
step: 3
---
## Q
分析 Java 程序时，JFR（Java Flight Recorder）和 async-profiler 各自的优势是什么？传统 Java 采样剖析器有什么偏差（safepoint bias）？

## A
**safepoint bias（安全点偏差）**：JVM 只能在**安全点**（safepoint，所有线程都停在已知状态的位置）读取线程的调用栈。传统的 Java 采样剖析器因此只在安全点取样，结果集中在有安全点检查的位置（循环末尾、方法返回处），而不是 CPU 真正耗时的位置，热点会被画歪。

- **JFR**：JVM 内置的事件记录器，开销很低（常用配置约 1%），能记录 GC 停顿、对象分配、锁竞争、线程阻塞、JIT 编译等 JVM 内部事件。适合在线上长期开着，事后分析“某段时间发生了什么”。
- **async-profiler**：通过操作系统的采样机制（Linux 的 `perf_events`）取样，不依赖安全点，因此**没有 safepoint bias**；还能同时看到 Java 栈、JVM 内部和内核/本地代码的栈，并支持按分配、按锁做剖析，输出火焰图。

经验：JFR 回答“JVM 里发生了什么”（GC、分配、停顿），async-profiler 回答“CPU 到底花在了哪些代码上”，两者互补。
