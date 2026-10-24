---
id: pl-memana-pitfall-rss
node: engineering.memory-analysis
type: qa
step: 8
---
## Q
堆剖析显示堆很小，进程内存（RSS）却不断上涨，可能是什么原因？怎么排查？

## A
RSS（resident set size，进程实际占用的物理内存）包含堆之外的很多东西：线程栈、元空间与代码缓存、**堆外内存**（off-heap）、C 库自己的分配、分配器碎片、运行时还没归还给操作系统的空闲页。堆剖析只看得到运行时管理的那一块。

**例**：Java 程序分配 300 个 1 MiB 的 direct buffer（`ByteBuffer.allocateDirect`，内存在 Java 堆之外），`-Xmx64m`，并保持引用：

```text
heap used MiB: 2
RSS MiB: 344
```

Java 堆只有 2 MiB，进程却占 344 MiB。堆转储和堆剖析在这里什么也发现不了。

**各语言的常见来源与手段**：
- Java：开 `-XX:NativeMemoryTracking=summary`，用 `jcmd <pid> VM.native_memory` 按类别（堆、元空间、线程、代码缓存、直接内存）列出；
- Go：用 `runtime.MemStats` 或运行时指标区分堆中使用、堆中空闲、栈。后台清扫线程（scavenger）逐步把空闲页还给系统，所以 RSS 的下降滞后于堆的下降；
- Python：小对象分配器的 arena 碎片会让对象释放后 RSS 不降；C 扩展泄漏对 `tracemalloc` 不可见，要用分配器层的工具（jemalloc 的剖析、heaptrack）；
- Rust：系统分配器的碎片，换 jemalloc 或 mimalloc 常有明显改善，再用 `dhat` 核对。

**规则**：先把「堆内指标」和 RSS 放在一起看。两条线分叉，就别再盯着堆剖析了，应该去找堆外。
