---
id: concurrency-thread-pool-backpressure
node: concurrency.patterns
type: qa
---
## Q
A fixed thread pool fed by an **unbounded** task queue never rejects work. What actually fails under sustained overload, and what's the disciplined setup?

## A
Nothing rejects, so nothing pushes back: the queue grows without limit — latency climbs (tasks wait behind thousands of others) and the process eventually **OOMs**. The failure is *hidden* until it's catastrophic.

- Disciplined: **bounded queue + explicit rejection policy**. `CallerRuns` is the classic backpressure choice — the submitter executes the task itself, naturally slowing producers.
- Size CPU-bound pools ≈ number of cores; IO-bound pools larger (≈ cores × (1 + wait/compute)).

Rule: overload must surface at the boundary, not accumulate in memory.

## Q zh
一个固定线程池，喂给它的是**无界**任务队列，于是它从不拒绝任务。持续过载下真正会失败的是什么，有纪律的配置该是什么样？

## A zh
没有任何东西被拒绝，也就没有任何东西往回推：队列无限增长 —— 延迟一路攀升（任务排在成千上万个任务后面），进程最终 **OOM**。这种失败在变成灾难之前是*看不见的*。

- 有纪律的做法：**有界队列 + 明确的拒绝策略**。`CallerRuns` 是经典的背压选择 —— 提交者自己去执行这个任务，自然而然地拖慢了生产者。
- 池大小：CPU 密集型 ≈ 核数；IO 密集型更大（≈ 核数 × (1 + 等待/计算)）。

规则：过载必须在边界处显现出来，而不是在内存里堆积。
