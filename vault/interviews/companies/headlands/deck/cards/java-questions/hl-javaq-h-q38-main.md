---
id: hl-javaq-h-q38-main
node: java-questions.h-ipc
type: qa
step: 1
---
## Q
同一台机器上进程间通信有哪些方式？比较管道、套接字、共享内存、消息队列、文件。
What are the ways processes can communicate on one machine? Compare pipes, sockets, shared memory, message queues, files.

## A
一句话：管道（单向字节流）、Unix 域 / TCP 套接字（双向、可跨机器）、**共享内存**（最快：零拷贝，但要自己同步）、消息队列、信号（通知）、文件。越靠近共享内存延迟越低、越要自己处理同步与崩溃恢复；越靠近套接字越通用、越慢。

- **管道 / FIFO**：进程 → 内核缓冲 → 进程（2 次拷贝），单向；Java 里是 `ProcessBuilder` 的 stdin / stdout。
- **套接字**（Unix 域 / TCP loopback）：加协议栈开销（TCP），双向，可换成跨机器；Java 16+ 支持 Unix 域套接字（JEP 380）。
- **共享内存**（mmap / `shm_open`）：同一物理页映射进两个进程，无拷贝，同步**自己做**，崩溃一方会留下半写状态。
- **消息队列**（POSIX / SysV）：有消息边界，Java 无标准 API。
- **信号**：只有通知，信息量极小。**文件**：慢、持久，用文件锁。
