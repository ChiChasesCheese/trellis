---
id: hi-c-lld-scarcity-n07-pool-timeout
node: lld.concurrency.scarcity.notes
type: qa
step: 7
---
## Q
**并发稀缺资源 · 超时与公平性**｜摘要 · 必会

`get()` 永远阻塞在请求路径上有什么危险？超时怎么设？等待者的顺序谁先谁后？

## A
- **危险：** 所有连接卡在慢查询时，新请求线程一直等，负载均衡器已超时，你的线程仍被占着
- **做法：** `get(timeout=...)`，超时抛 `queue.Empty`，转换成自己的异常；调用方返回 503、重试或记录
- **超时取值：** 太短会误杀本可成功的请求，太长让用户干等；查询通常 100 毫秒就设 500 毫秒，且小于客户端或负载均衡器的超时
- **公平性：** 等待顺序大致先来先服务；需要严格保证时用公平队列（Java 的 `ArrayBlockingQueue(fair=true)`），吞吐会降低
