---
id: hft-java-off-heap-directbuf-pitfalls
node: java.off-heap
type: qa
step: 3
---
## Q
DirectByteBuffer 在容量和释放上有哪两个结构性问题？会怎样出事？

## A
① **容量用 `int`**：最大约 2 GB。想要 3 GB 的表，`allocateDirect((int) 3_000_000_000L)` 会因为强转溢出成负数而抛 `IllegalArgumentException`，只能拆成多个 buffer。

② **没有 `close()`**：堆外内存要等 GC 发现这个 `ByteBuffer` 对象不可达后，由 Cleaner 释放。如果堆里很空、GC 很久不触发，堆外内存迟迟不归还，一旦到达 `-XX:MaxDirectMemorySize` 上限就抛 `OutOfMemoryError: Direct buffer memory`，而此时 Java 堆可能还剩很多。

另外它没有结构，偏移量全靠手算，容易写成魔法数字。所以高频地分配和丢弃 DirectByteBuffer 是反模式，应该启动时分配一次长期持有。
