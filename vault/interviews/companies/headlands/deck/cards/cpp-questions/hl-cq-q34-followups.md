---
id: hl-cq-q34-followups
node: cpp-questions.h-os
type: qa
step: 15
---
## Q
三个追问：共享内存里消费者怎么知道有数据了？进程共享互斥量怎么设置？为什么不直接用套接字？

## A
- **怎么知道有数据**：自旋读原子索引（延迟最低），或空闲时阻塞在信号量 / eventfd / futex 上。
- **进程共享互斥量**：`pthread_mutexattr_setpshared(PTHREAD_PROCESS_SHARED)`；Linux 上再加 robust 互斥量，用来从持有者死亡中恢复。
- **为什么不用套接字**：套接字每条消息一次系统调用加一次拷贝；每秒百万条小消息时共享内存更优。
