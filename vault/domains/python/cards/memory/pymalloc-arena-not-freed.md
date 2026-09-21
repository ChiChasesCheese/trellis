---
id: pymalloc-arena-not-freed
node: memory.allocator
type: qa
tags: [grown]
source: python-docs
---
## Q
长驻的 Python 进程把大量对象 `del` 掉之后，为什么进程的 RSS（常驻内存）常常不会跌回去？

## A
pymalloc 只有当一个 arena（约 1 MiB 的大块内存）里的所有 pool 都完全空闲时，才会把这整个 arena 归还给操作系统；只要这个 arena 里还有一个 pool 挂着哪怕一个存活对象，整块 arena 就继续占着不放。长驻进程里对象分配和释放会不断交织，很容易出现“每个 arena 都零散挂着一两个存活对象”的碎片化局面，于是已经不再使用的内存迟迟还不回操作系统，RSS 居高不下。
