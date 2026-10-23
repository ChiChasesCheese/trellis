---
id: hl-cq-q33-ipc-methods
node: cpp-questions.h-os
type: qa
step: 7
---
## Q
面试题：你知道哪些进程间通信（IPC）方式？分别在什么时候选？
What IPC (inter-process communication) methods do you know? When would you pick each?

## A
方式：管道（pipe / FIFO）、Unix 域套接字和 TCP / UDP 套接字、共享内存、消息队列、信号、文件 / `mmap`。
- **共享内存最快**：稳态下没有系统调用、没有拷贝，但同步要自己做。
- **套接字最通用**：可以跨机器。
- **管道最简单**。
- 同机、延迟敏感的交接：共享内存加无锁队列；控制类流量用套接字。
- 不管选哪个，都要处理**部分读**（partial reads）、字节流上的**消息边界**，以及关闭不用的描述符。
