---
id: hl-os-ring-real-world
node: foundations.os-processes-threads-ipc
type: qa
step: 32
---
## Q
真实世界里有哪些和 SPSC 环形缓冲同类的东西？

## A
- **Agrona** 的 `OneToOneRingBuffer` / `ManyToOneRingBuffer`：变长消息版的共享内存环形缓冲；
- **Aeron** 的 IPC 通道：同机进程通过映射文件里的日志缓冲区通信，延迟百纳秒量级；
- **Chronicle Queue**：映射文件上的追加日志，既是 IPC 又是持久化日志；
- **LMAX Disruptor**：同一 JVM 内线程间的环形缓冲（有序号、等待策略、缓存行填充）；
- **Linux io_uring**：内核与用户态之间的提交队列（SQ）和完成队列（CQ）是映射在共享内存里的 SPSC 环形缓冲，用户态写 SQ、内核读，内核写 CQ、用户态读，省掉每次 I/O 的系统调用。
