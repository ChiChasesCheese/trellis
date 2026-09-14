---
id: runtime-go-concurrency-bounded-fanout
node: runtimes.go-concurrency
type: qa
---
## Q
A cache miss launches one goroutine per candidate origin. Under an outage, goroutine count and memory grow without bound. What control is missing?

## A
Goroutines are cheap, not free; unbounded fan-out converts dependency slowness into local resource exhaustion. Add a bounded semaphore or worker pool, acquire it before launching work, and reject or degrade when capacity is full. Tie every worker to the request `Context`, cap the queue, and expose in-flight and rejected counts. The bound should represent the downstream's safe concurrency, not the machine's maximum goroutine count.

## Q zh
cache miss 会为每个候选 origin 启动一个 goroutine。故障期间 goroutine 数和内存无限增长。缺少什么控制？

## A zh
Goroutine 很便宜，但不是免费；unbounded fan-out 会把 dependency 变慢转换成本地资源耗尽。应在启动工作前获取 bounded semaphore 或进入有界 worker pool；容量满时 reject 或 degrade。每个 worker 都绑定 request `Context`，queue 必须有上限，并暴露 in-flight 与 rejected 数。这个上限应代表 downstream 的安全并发度，而不是机器能承受的最大 goroutine 数。
