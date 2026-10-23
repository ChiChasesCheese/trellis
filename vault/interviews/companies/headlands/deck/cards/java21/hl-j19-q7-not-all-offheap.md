---
id: hl-j19-q7-not-all-offheap
node: java21.j19-runtime-zgc-jit
type: qa
step: 40
---
## Q
面试问：为什么不直接把所有东西放堆外？
Why not put everything off-heap?

## A
- 堆外去掉了这部分数据的 GC 成本，但要付代价：**手动管理生命周期**、**没有自动扩容**、**边界检查开销**、代码更复杂；
- 只对**大的、长寿的、固定布局**的表这么做，如 ticker map 或池化的成交记录；
- 前提：先 profile，**确认 GC 是瓶颈**再做。

英文骨架：「Off-heap removes GC cost for that data, but you pay with manual lifecycle, no auto-resizing, bounds checks and complexity. Only for large, long-lived, fixed-layout tables, after profiling shows GC is the bottleneck.」

边界：不要在面试里编造面试公司自己的技术栈；被问「你们用什么 GC」可答「我了解 ZGC 与 G1 的取舍，我会在目标负载上测」。
