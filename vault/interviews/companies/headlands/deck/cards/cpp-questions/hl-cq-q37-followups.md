---
id: hl-cq-q37-followups
node: cpp-questions.i-low-latency
type: qa
step: 10
---
## Q
三个追问：怎么把 SPSC 改成 MPSC 或 MPMC？为什么不用 `seq_cst`？无锁（lock-free）和无等待（wait-free）的区别？

## A
- **MPSC / MPMC**：生产者用原子 `fetch_add` 或 CAS 抢占槽位，并为每个槽位发布序号；争用和复杂度都更高；或者每个生产者一条 SPSC 队列。
- **不用 `seq_cst`**：交接用 acquire / release 就足够，在弱序 CPU 上更便宜。
- **lock-free**：总有某个线程在前进；**wait-free**：每个线程都在有限步内完成。
