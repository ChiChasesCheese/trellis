---
id: hft-java-tuning-affinity
node: java.tuning
type: qa
step: 3
---
## Q
低延迟 Java 里怎样把线程绑定到固定的 CPU 核（线程绑核，thread affinity）？为什么要这样做？

## A
Java 标准库没有绑核的接口。常用 OpenHFT 的 Java-Thread-Affinity 库，它通过 JNA 调用 Linux 的 `sched_setaffinity`，用法如 `AffinityLock.acquireCore()`。

为什么要绑：热线程如果被操作系统在核之间迁移，L1/L2 缓存里积累的热数据就作废，等于每次迁移后重新“冷启动”缓存；迁移本身还有上下文切换的开销。绑核再配合内核参数把这些核隔离出来（不让别的任务和中断打扰），热线程就能稳定、可预期地运行。

常见布局：每个自旋的热线程独占一个核；GC 线程和 JIT 编译线程放到别的核（用 `-XX:ConcGCThreads`、`-XX:CICompilerCount` 控制数量），避免和热线程抢核。
