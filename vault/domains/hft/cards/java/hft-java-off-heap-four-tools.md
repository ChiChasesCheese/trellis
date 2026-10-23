---
id: hft-java-off-heap-four-tools
node: java.off-heap
type: qa
step: 2
---
## Q
Java 里放堆外数据有 DirectByteBuffer、`sun.misc.Unsafe`、FFM API、内存映射文件四种常见方式，它们各自的特点是什么？

## A
| 方式 | 特点 |
|---|---|
| DirectByteBuffer | Java 1.4 起；容量是 `int`，最大约 2 GB；没有 `close()`，靠 GC 之后的 Cleaner 释放 |
| `Unsafe` | 直接按地址读写，最快也最危险；无边界检查，越界就崩进程；属于内部 API，JDK 在逐步收紧 |
| FFM API | JDK 22 正式；`Arena` 管生命周期，`MemorySegment` 带边界检查，大小是 `long`，可立即释放 |
| 内存映射文件（mmap） | 把文件映射进地址空间，可持久化、可跨进程共享；Java 里用 `FileChannel.map` 或 FFM |

新代码优先选 FFM；需要持久化或跨进程共享时用 mmap。
