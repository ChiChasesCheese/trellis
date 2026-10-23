---
id: hl-j16-false-sharing
node: java21.j16-concurrency-primitives
type: qa
step: 24
---
## Q
什么是伪共享（false sharing）？缓存行多大？怎么避免和检测？

## A
CPU 缓存按**缓存行**搬运和保持一致（x86 常见 **64 字节**，Apple M 系列 **128 字节**）。线程 A 只改 `a`、线程 B 只改 `b`，而 `a`、`b` 恰在**同一缓存行**：A 写一次，该行在 B 的核里失效；B 写一次又让 A 的失效。两个互不相干的变量在硬件层面抢同一块东西。

避免：让它们相隔至少一条缓存行（**填充**，padding）；JDK 内部用 `@jdk.internal.vm.annotation.Contended`，用户类需 `-XX:-RestrictContended`；或每线程用自己的状态再合并（`LongAdder` 思路）。

检测：性能剖析看缓存未命中、`perf c2c`，或做对照实验。只在高频写、多线程、相邻变量时显现，先用 profiler 确认，别预先到处填充。
