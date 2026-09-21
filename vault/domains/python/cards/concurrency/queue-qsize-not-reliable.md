---
id: queue-qsize-not-reliable
node: concurrency.queues
type: qa
source: python-docs
---
## Q
为什么 `queue.qsize() > 0` 之后紧接着调用 `get()`，仍然可能阻塞？

## A
`qsize()`、`empty()`、`full()` 返回的都只是调用那一刻的近似值（approximate）。在多线程环境下，从你读到这个值到你真正调用 `get()`/`put()` 之间，其他线程可能已经并发地修改了队列内容——这是典型的“检查后再操作”（check-then-act）竞态：检查和操作之间不是原子的。因此这些方法只能用于监控/调试，不能用来判断后续的阻塞操作是否会执行，实际代码应该直接调用 `get()`/`put()` 并处理其阻塞或超时行为。
