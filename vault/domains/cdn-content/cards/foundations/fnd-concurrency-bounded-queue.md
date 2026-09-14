---
id: fnd-concurrency-bounded-queue
node: foundations.concurrency
type: qa
---
## Q
Why is an unbounded request queue an availability bug, and what should happen when a serving tier reaches capacity?

## A
An unbounded queue converts overload into growing memory use and ever-longer latency until the process crashes; most queued requests will miss their deadlines anyway. Use a small bounded queue or direct concurrency limit, reject early with a retryable signal, preserve capacity for critical work, and expose queue depth plus wait time.

## Q zh
为什么 unbounded request queue 是 availability bug？serving tier 到达 capacity 后应该发生什么？

## A zh
unbounded queue 会把 overload 变成持续增长的 memory 与 latency，直到进程崩溃；而大部分排队请求最终也会错过 deadline。使用小型 bounded queue 或直接 concurrency limit，尽早返回可 retry 的拒绝信号，为 critical work 保留 capacity，并暴露 queue depth 与 wait time。
