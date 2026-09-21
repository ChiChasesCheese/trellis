---
id: mp-bypasses-gil-needs-pickle
node: concurrency.multiprocessing
type: qa
source: python-docs
---
## Q
`multiprocessing` 如何绕过 GIL 实现真正的并行，代价是什么？

## A
每个 `Process` 都是独立的操作系统进程，拥有自己的 Python 解释器和自己的 GIL，因此多个进程能在不同 CPU 核心上真正同时执行字节码。代价是进程间没有共享内存：`Process` 的参数、`Queue`/`Pipe` 传递的对象、`Pool` 任务的参数和返回值都必须可被 pickle 序列化——不可 pickle 的对象（如某些锁、打开的文件句柄、lambda）无法跨进程传递，传递大对象也有序列化/反序列化的额外开销。
