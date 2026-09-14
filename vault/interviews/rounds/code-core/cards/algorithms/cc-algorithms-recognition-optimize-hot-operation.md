---
id: cc-algorithms-recognition-optimize-hot-operation
node: algorithms.recognition
type: qa
---
## Q
How do you choose the data structure before writing the loop?

## A
**Name the operation the program repeats most, then pick the structure that makes *that* operation cheap.** Everything else can stay a list.

- "least loaded, per request" → heap ([[cc-toolbox-heap-lazy-invalidation]]); "does this id exist" → set; "count in a range" → prefix sums or `bisect`; "value at time t" → sorted times plus `bisect`; "same group?" → union-find; "next greater" → monotonic stack.
- Count the repetitions straight from the constraints: 10^5 requests × 10^5 candidates is 10^10, so the per-request operation must be sub-linear ([[cc-algorithms-recognition-constraint-sizes]]).
- Optimizing a cold path costs minutes and buys nothing; a structure chosen for elegance rather than for the hot operation costs both.
- If two operations are both hot and want different structures, keep two indexes and accept the cost of keeping them in step.

## Q zh
在写循环之前，你怎么选数据结构？

## A zh
**说出程序重复得最多的那个操作，然后选让*那个*操作变便宜的结构。** 其余一切都可以保持是 list。

- 「每个请求求负载最小」→ 堆（[[cc-toolbox-heap-lazy-invalidation]]）；「这个 id 存在吗」→ set；「区间内计数」→ 前缀和或 `bisect`；「t 时刻的值」→ 有序时间加 `bisect`；「同一组吗」→ 并查集；「下一个更大值」→ 单调栈。
- 直接从约束里算重复次数：10^5 个请求 × 10^5 个候选就是 10^10，所以每请求的操作必须是次线性的（[[cc-algorithms-recognition-constraint-sizes]]）。
- 优化冷路径花时间且毫无收益；为优雅而非为热点操作挑的结构则两头都赔。
- 如果两个操作都很热且需要不同结构，就维护两个索引，并接受让它们保持同步的代价。
