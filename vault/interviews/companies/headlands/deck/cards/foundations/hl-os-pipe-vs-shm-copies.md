---
id: hl-os-pipe-vs-shm-copies
node: foundations.os-processes-threads-ipc
type: qa
step: 16
---
## Q
为什么说管道要拷贝两次而共享内存零拷贝？

## A
管道或 socket：进程 A 的缓冲区 ──`write()`──▶ 内核缓冲区（拷贝 1）──`read()`──▶ 进程 B 的缓冲区（拷贝 2），共两次系统调用。

共享内存：进程 A 和进程 B 的页表都指向同一块物理内存页，A 写、B 读，**没有拷贝，也不经过内核**，建立映射之后没有系统调用。
