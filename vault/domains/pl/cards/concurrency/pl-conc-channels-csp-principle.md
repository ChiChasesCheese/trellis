---
id: pl-conc-channels-csp-principle
node: concurrency.channels-csp
type: qa
step: 1
---
## Q
什么是通道（channel）和 CSP？为什么说「通过通信来共享内存，而不是通过共享内存来通信」？通道的设计空间有哪些？

## A
**问题**：多个线程直接读写同一块内存，就要用锁保护，漏一处就是数据竞争（data race），而且很难推理「谁在什么时候改了它」。

**CSP**（Communicating Sequential Processes，通信顺序进程，Hoare 1978）换一种思路：每个任务有自己的私有数据，任务之间只通过**通道**传递消息。通道是一个带同步功能的队列：一端 `send`，另一端 `receive`。数据通过通道交出去之后，发送方不再使用它，同一时刻只有一个任务拥有它，竞争就没有了。口号是 Go 的：「不要通过共享内存来通信，而要通过通信来共享内存」。

**通道的设计选择**：
1. **同步程度**：无缓冲（unbuffered，容量 0）要求发送方和接收方「碰头」才完成（rendezvous）；有缓冲（buffered）允许发送方先放入 N 个再继续。
2. **有界还是无界**：有界队列满了会让发送方阻塞，形成**背压**（backpressure，下游慢时反过来让上游慢下来）；无界队列永远不阻塞，但生产快于消费时内存会一直涨。
3. **端点数量**：多生产者单消费者（mpsc）还是多对多。
4. **关闭语义**：发送方说「没有更多数据了」，接收方怎样知道结束。

不是所有语言都内置通道：Go 把它做进语法（`chan`、`<-`、`select`）；Rust、Java、Python 是库（`mpsc`、`BlockingQueue`、`queue.Queue`）。
