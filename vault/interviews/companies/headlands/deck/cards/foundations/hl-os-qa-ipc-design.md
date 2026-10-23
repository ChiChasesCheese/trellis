---
id: hl-os-qa-ipc-design
node: foundations.os-processes-threads-ipc
type: qa
step: 38
---
## Q
面试题：同机两个进程要传高频小消息，怎么设计？

## A
推荐答法：共享内存加 SPSC 环形缓冲。
- 映射同一个文件（Linux 放 `/dev/shm`）；
- `head` 和 `tail` 各占一条缓存行避免伪共享，序号只增不减，槽位用 `序号 & mask`；
- 生产者先写数据再 release 写 `tail`；消费者 acquire 读 `tail`、读数据、再 release 写 `head`；每个变量单写者，无锁无 CAS；
- Java 里用 FFM 的 `MemorySegment` 加 `VarHandle`；我测过两个进程传 5000 万条，每秒几千万到上亿条。
