---
id: hl-cq-q33-script
node: cpp-questions.h-os
type: qa
step: 10
---
## Q
用英文 60 秒回答：What IPC (inter-process communication) methods do you know? When would you pick each?

## A
结构：列出方式 → 管道最简单、Unix 套接字双向可传描述符、TCP 跨机最慢 → 共享内存最快但自己同步（无锁环形缓冲）→ 本机低延迟选共享内存，控制流量用套接字，处理部分读与消息边界。

- The main options are **pipes** and FIFOs, **Unix domain sockets** and TCP/UDP sockets, **shared memory**, message queues, signals, and memory-mapped files.
- Pipes are simplest - one direction, related processes. Unix sockets are bidirectional and can pass file descriptors. TCP works across machines but is slowest.
- **Shared memory is the fastest** because after setup there are no system calls and no copies - both processes map the same physical pages - but I have to provide synchronization myself, for example atomics in a ring buffer.
- For a latency-critical hand-off on one machine I would choose shared memory with a lock-free queue; for control traffic, sockets. Whichever I choose, I must handle **partial reads**, message framing on byte streams, and closing unused descriptors.
