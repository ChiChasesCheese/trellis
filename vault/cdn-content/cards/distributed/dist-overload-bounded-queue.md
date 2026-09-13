---
id: dist-overload-bounded-queue
node: distributed.overload
type: qa
---
## Q
Why does an unbounded request queue make an overloaded service look available while making outcomes worse?

## A
It accepts work the service cannot finish before deadlines. Queueing delay grows, memory rises, clients time out and retry, and CPU is spent on expired requests. Bound queue and in-flight concurrency, reject early with a retryable overload signal, and use remaining-deadline admission. A short controlled error preserves capacity for work that can succeed; a long queue converts overload into high-latency failure.

## Q zh
为什么 unbounded request queue 会让 overload service 看似可用，却让结果更差？

## A zh
它接受了 service 无法在 deadline 前完成的工作。queueing delay 增长、内存上涨、client timeout 并 retry，CPU 又消耗在已过期请求上。应限制 queue 和 in-flight concurrency，尽早返回可 retry 的 overload signal，并按 remaining deadline admission。短而受控的 error 能为可成功工作保留 capacity；长 queue 则把 overload 转成 high-latency failure。
