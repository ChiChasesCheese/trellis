---
id: hl-javaq-f-q32-say60
node: java-questions.f-concurrency
type: qa
step: 37
---
## Q
用英文 60 秒回答：How do you size a thread pool? What are the pitfalls of `Executors`?

## A
结构：CPU 密集看核数，I/O 密集看等待比或用虚拟线程 → Little 定律校验 → Executors 的无界队列与无界线程 → ThreadPoolExecutor 的处理顺序 → 有界队列、背压、命名、关闭。

> "For CPU-bound work I'd use about the number of cores; for I/O-bound work, cores times one plus wait over compute, or just virtual threads. Little's law is the sanity check: concurrency equals throughput times latency. The pitfalls are in `Executors`: the fixed pool has an unbounded queue and the cached pool has unbounded threads, so overload turns into out-of-memory. With `ThreadPoolExecutor` the order is core threads, then queue, then up to max, then reject - so an unbounded queue means max is never used. I'd use a bounded queue, a rejection policy that applies back-pressure, named threads, and proper shutdown. In my test a 200-thread pool doing one-second blocking tasks capped out at 200 tasks per second regardless of CPU count."
