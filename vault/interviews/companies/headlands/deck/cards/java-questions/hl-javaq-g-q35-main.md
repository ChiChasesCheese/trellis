---
id: hl-javaq-g-q35-main
node: java-questions.g-os
type: qa
step: 4
---
## Q
解释虚拟内存、page cache 和缺页（page fault）。为什么 JVM 的 RSS 比 `-Xmx` 大？
Explain virtual memory, the page cache and page faults. Why is a JVM's RSS bigger than `-Xmx`?

## A
一句话：每个进程看到自己的**虚拟地址空间**，MMU 通过页表（TLB 缓存翻译）映射到物理页；访问没映射的页触发**缺页**，内核按需分配（匿名页：分配并清零）或从文件读入；文件 I/O 先经过 **page cache**（内核缓存）：写先写 page cache，稍后回写，`fsync` 强制落盘。

JVM 的 RSS = 堆 + 元空间 + 代码缓存 + 线程栈 + GC 数据结构 + 直接内存 + 共享库，所以必然大于 `-Xmx`。

排查：`-XX:NativeMemoryTracking=summary` + `jcmd <pid> VM.native_memory summary`；Linux 上看 `/proc/<pid>/smaps`、`pmap`。
