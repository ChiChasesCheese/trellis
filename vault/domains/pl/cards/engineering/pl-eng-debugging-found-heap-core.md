---
id: pl-eng-debugging-found-heap-core
node: engineering.debugging
type: qa
step: 4
---
## Q
内存持续上涨时，怎么知道是谁在占内存？Java 的类直方图、Python 的 `tracemalloc`、堆转储和核心转储分别提供什么信息？

## A
**内存泄漏**在 GC 语言里的意思不是“忘了释放”，而是“还被引用着但再也不会被用”：最常见的是一个永远不清理的缓存或全局 Map。

**Java 类直方图**（`jcmd <pid> GC.class_histogram`）：按类统计存活对象数与字节数。对一个把 5 万个会话塞进永不淘汰的 `HashMap` 的程序：
```
 num   #instances   #bytes  class name
   1:     158520  54782920  [B (byte arrays)
   2:     108442   2602608  java.lang.String
   4:      50000   1200000  Leak$Session
```
`Leak$Session` 恰好 5 万个，字节数组占了 54 MB，一眼就知道是会话对象带着缓冲区。注意：这条命令默认先触发一次 Full GC，所以统计的是**真正存活**的对象。

**堆转储**（`jcmd <pid> GC.heap_dump file.hprof`，再用 Eclipse MAT 或 VisualVM 打开）：保存整个堆。它多回答一个问题：**谁在引用这些对象**（引用链，到 GC 根的最短路径）。堆越大转储越慢、文件越大，线上要提防暂停。`-XX:+HeapDumpOnOutOfMemoryError` 让 JVM 在 OOM 时自动生成。

**Python**：`tracemalloc` 记录每块内存是在哪一行分配的：
```python
tracemalloc.start()
# ... code that fills an unbounded dict ...
tracemalloc.take_snapshot().statistics("lineno")[0]
# tm.py:4: size=21.2 MiB, count=40003, average=555 B
```
**Go**：`pprof` 的 heap profile（采样记录分配调用栈）；**Rust** 没有 GC，泄漏多半来自引用计数环（`Rc` 互相引用）或无限增长的容器，用 `valgrind`/`heaptrack`/`dhat` 定位。

**核心转储**（core dump）是进程崩溃时整个内存的镜像，可以用调试器事后查看崩溃时的栈与变量。Go 需要设置 `GOTRACEBACK=crash`，Linux 上还要 `ulimit -c unlimited`；它适合“崩了但没法复现”的 native 问题（Rust 的 `unsafe`、cgo），对 JVM 和 Python 常常不如专用转储。

**步骤**：先用直方图/`tracemalloc` 看“增长的是什么”，再用堆转储看“谁拿着它”。
