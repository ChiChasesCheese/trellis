---
id: pl-conc-channels-csp-mechanism
node: concurrency.channels-csp
type: qa
step: 6
---
## Q
Go 的 channel 在运行时内部是怎样实现的？无缓冲与有缓冲在阻塞行为和速度上有什么区别？

## A
一个 Go channel 在运行时是一个结构体（`hchan`），包含：
- 一个环形缓冲区（容量 = `make(chan T, n)` 的 n，无缓冲时为 0）；
- 一把互斥锁，保护整个结构；
- 两个等待队列：**sendq**（因为缓冲区满而阻塞的发送方 goroutine）和 **recvq**（因为缓冲区空而阻塞的接收方）。

发送 `ch <- v` 的步骤：
1. 如果 recvq 里已有等着的接收方，直接把 `v` 拷给它并唤醒它，不经过缓冲区（这就是无缓冲通道的「碰头」）。
2. 否则如果缓冲区有空位，把 `v` 放进去，立刻返回。
3. 否则当前 goroutine 挂进 sendq 并让出线程（只挂起 goroutine，线程不阻塞）。

接收是对称的。关闭通道会唤醒全部等待者：接收方读到零值和 `ok=false`，发送方 panic。

速度（一台 12 核 Mac，生产者与消费者各一个 goroutine，一次测量）：
- 无缓冲：约 70 纳秒 / 条。每条都要把对方叫醒、切换 goroutine。
- 容量 1024：约 16 纳秒 / 条。绝大多数发送只是写缓冲区，一次唤醒摊给一批元素。

对照：Rust `mpsc` 约 14–17 纳秒 / 条，Java `ArrayBlockingQueue(1024)` 约 180 纳秒 / 条（锁 + 条件变量），Python `queue.Queue(1024)` 约 360 纳秒 / 条。

规律：通道不是免费的，每次操作要加锁；批量放入、合理的缓冲会明显降低成本。
