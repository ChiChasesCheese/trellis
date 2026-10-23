---
id: hl-javaq-h-q39-robustness
node: java-questions.h-ipc
type: qa
step: 6
---
## Q
共享内存 IPC 要处理哪些健壮性问题（崩溃一致性、对齐字节序、生命周期、生产上的选择）？消费者比生产者慢怎么办？为什么不能用 `synchronized` 跨进程同步？
Why not use `synchronized`/locks across processes?

## A
- **崩溃一致性**：对方写一半崩溃 → 用序号 + 校验和，消费者能发现半写记录；重启时从 head / tail 恢复。
- **对齐与字节序**：用 `ByteOrder.nativeOrder()`；定长记录（`StructLayout`）避免序列化。
- **生命周期**：`MappedByteBuffer` 没有显式 unmap；删除文件后映射仍有效，直到最后一个映射消失。21 里 FFM（`MemorySegment`、`Arena`）可替代，并用 `long` 下标突破 2 GB 限制。
- **生产上**多用现成库（Chronicle Queue、Aeron IPC）而不是手写。
- **消费者太慢**：环满，生产者等待 / 丢弃 / 背压；序号差即队列深度。
- **不能用 `synchronized`**：JVM 内的锁只在本进程内有效；跨进程要用文件锁或基于共享内存的原子协议。
