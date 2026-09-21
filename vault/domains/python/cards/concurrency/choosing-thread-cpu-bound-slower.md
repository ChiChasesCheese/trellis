---
id: choosing-thread-cpu-bound-slower
node: concurrency.choosing
type: qa
tags: [grown]
---
## Q
为什么给一个 CPU 密集型的纯 Python 任务加上多线程，实际运行时间反而可能比单线程更长？

## A
CPU 密集任务里线程几乎不会主动释放 GIL（没有阻塞 I/O 调用），因此多个线程之间要靠解释器按切换间隔强制换出 GIL 来分时执行，本质上仍是串行执行字节码；而额外引入的线程创建、上下文切换、GIL 的获取与释放本身都有开销。结果是总的有效计算时间没有变化，却多付出了线程调度和 GIL 争用的开销，总耗时不降反升。这种任务应该改用多进程或释放 GIL 的 C 扩展库。
