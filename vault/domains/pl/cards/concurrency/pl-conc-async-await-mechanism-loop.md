---
id: pl-conc-async-await-mechanism-loop
node: concurrency.async-await
type: qa
step: 4
---
## Q
事件循环内部是怎样同时等待上万个连接的？“就绪队列”、“选择器”、“唤醒”分别是什么？实测 1 个线程能承载多少个并发等待？

## A
事件循环在一个线程里反复做同一件事，核心是两个数据结构：
1. **就绪队列**（ready queue）：现在就能继续运行的任务。循环取出一个，运行到它下一个 `await`（挂起点），再取下一个。
2. **选择器**（selector）：操作系统提供的“多路复用”接口（Linux `epoll`、macOS `kqueue`），让一个线程**同时监视成千上万个文件描述符**：“这些套接字里谁可读/可写了？”以及“最近的定时器还要多久到期？”。

循环每一轮：
- 就绪队列非空：先跑完队列里的任务；
- 队列空了：调用 `selector.select(timeout)`，**阻塞线程**直到“某个连接就绪”或“最近的定时器到期”；
- 把就绪的连接对应的任务（它们之前在 `await` 这些 I/O 时挂起）放回就绪队列，把到期的定时器任务放回队列；
- 回到开头。

所以线程只在“无事可做”时才阻塞，并且是被内核高效唤醒，而不是忙等。`await asyncio.sleep(d)` 其实就是向循环登记一个定时器，然后挂起当前任务。Python 的循环类型和选择器可以直接查看：在 macOS 上是 `_UnixSelectorEventLoop` + `KqueueSelector`。

Rust 的 tokio 同理：reactor 线程使用 `epoll/kqueue`，通过 `Waker` 把就绪的 `Future` 放回执行器的队列。

实测（一次测量）：
- Python：一个线程同时运行 10000 个各 `await asyncio.sleep(0.1)` 的任务，总耗时 **0.13 秒**；
- Rust tokio（单线程运行时）：10000 个任务各 `sleep(100ms)`，总耗时 **0.29 秒**。
一个线程承载上万个并发等待，而同样数量的 OS 线程会撞上系统上限。

局限：循环只有一个线程在跑 Python 代码，任何**不 `await` 的耗时操作**都会让整个队列停摆；多核要靠多个事件循环（多进程、多线程）。
