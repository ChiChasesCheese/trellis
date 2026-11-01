---
id: hi-sd-temporal-7-sticky
node: sd.deep-dives.temporal
type: qa
step: 7
---
## Q
**避免每次都重放：缓存与粘性执行**｜系统设计 · 关键技术

Temporal 靠重放历史来恢复状态，但一个长工作流每次有事件都从头重放太贵。它怎样优化，缓存失效或 Worker 崩溃时正确性如何保证？

## A
**做法。** Worker 首次拿到某工作流任务时用历史重建状态，并把它缓存在内存里（Workflow Cache）。之后 Temporal 尽量把同一工作流的后续任务送回同一个 Worker，这叫粘性执行（Sticky Execution）：Worker 同时轮询普通任务队列和自己专属的粘性队列。

**正确性。** 缓存只是优化。Worker 崩溃或缓存被淘汰时，下一个工作流任务回到普通队列，任何可用 Worker 都能从持久历史重建状态。

**一句话。** 事件历史保证正确，缓存和粘性执行换来性能。

**要点。** 这是典型的“持久日志做真相，内存缓存做加速”的设计，面试里讲 Temporal 内部不是必需，了解即可。
