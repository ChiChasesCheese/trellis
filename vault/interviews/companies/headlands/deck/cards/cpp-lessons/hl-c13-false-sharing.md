---
id: hl-c13-false-sharing
node: cpp-lessons.c13-memory-model-atomics
type: qa
step: 13
---
## Q
面试问：什么是伪共享（false sharing）？怎么发现和避免？
Interview question: What is false sharing?

## A
- 缓存一致性协议（MESI）以**缓存行**为单位工作（x86 通常 64 字节；一些 ARM 芯片 128 字节）。
- 两个线程写**不同的变量**，只要落在同一缓存行，每次写都会让对方核心那一行失效，缓存行在核心之间来回弹跳，性能崩溃，尽管没有任何逻辑共享。
- 发现：`perf` 看缓存未命中 / 一致性流量。
- 避免：对齐/填充 `alignas(64)`（或 `std::hardware_destructive_interference_size`）；每线程私有再合并。代价是浪费内存，只对热点变量用。
