---
id: hl-c13-selftest-cacheline
node: cpp-lessons.c13-memory-model-atomics
type: qa
step: 18
---
## Q
自测：为什么 SPSC 队列的 `head_` 和 `tail_` 要放在不同缓存行？

## A
- 它们分别由消费者和生产者两个线程**频繁写**；放在同一缓存行会导致**伪共享**，缓存行在两个核心间来回失效。
- 做法：`alignas(64)` 把 `head_`、`tail_` 和缓冲区各放独立缓存行。
