---
id: fnd-concurrency-parallelism
node: foundations.concurrency
type: qa
---
## Q
A proxy increases in-flight requests from 100 to 10,000 but throughput barely changes and latency explodes. Why did more concurrency not create more parallelism?

## A
**Concurrency** is how many tasks are in progress; **parallelism** is how many execute at once on available CPU, I/O, or downstream capacity. Once the bottleneck is saturated, extra in-flight work only waits in queues, consumes memory, and worsens tail latency. Bound concurrency near measured service capacity and shed excess load.

## Q zh
proxy 把 in-flight request 从 100 提高到 10,000，但 throughput 几乎不变、latency 暴涨。为什么更多 concurrency 没有带来更多 parallelism？

## A zh
**Concurrency** 是同时处于进行中的任务数；**parallelism** 是受 CPU、I/O 或 downstream capacity 限制、真正同时执行的任务数。bottleneck 饱和后，额外 in-flight work 只会进入 queue、消耗 memory，并恶化 tail latency。应该把 concurrency 限制在实测 service capacity 附近，并对超额负载做 load shedding。
