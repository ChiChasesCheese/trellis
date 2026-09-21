---
id: mp-queue-vs-pipe
node: concurrency.multiprocessing
type: qa
source: python-docs
---
## Q
`multiprocessing.Queue` 和 `multiprocessing.Pipe()` 都能在进程间传递数据，什么时候用哪个？

## A
`Queue` 是 `queue.Queue` 的近似克隆，天然支持多个生产者、多个消费者并发读写，内部已处理好同步，适合多对多的任务分发场景。`Pipe()` 返回一对通过管道连接的连接对象（默认双工），更轻量、延迟更低，但只设计给两端各自的一个读者/写者使用——如果多个进程（或线程）同时读写管道的*同一端*，数据可能被破坏（corrupted），因此 `Pipe` 适合两个进程间的一对一通信，多对多场景应该用 `Queue`。
