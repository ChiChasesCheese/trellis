---
id: hl-javaq-rubric-h-ipc
node: java-questions.rubric
type: qa
step: 12
---
## Q
回答进程间通信（IPC）的问题时，强、一般、弱的答案各有什么特征？

## A
- **强**：列出管道 / 套接字 / 共享内存 / 消息队列 / 信号 / 文件，并说出数据路径（拷贝次数）与同步责任；共享内存最快但要自己同步、处理对端崩溃；Java 里用 `MappedByteBuffer` + `VarHandle`（或 FFM），SPSC 环形缓冲、head / tail 分缓存行、release / acquire；有数量级（管道约 3 µs、loopback TCP 约 12 µs、共享内存约 0.15 µs）。
- **一般**：能列出方法并比较快慢；对 Java 实现没有想法，或只知道 `Socket`。
- **弱**：说"IPC 就是 socket"；认为 `ByteBuffer.putLong` 在两个进程间自动可见；认为 JVM 内的 `synchronized` 能锁住别的进程。
