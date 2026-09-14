---
id: cc-performance-hot-loop-resort
node: performance.hot-loop
type: qa
---
## Q
After every event your code calls `sorted(candidates)` (or `min(...)` over everything) to find the next winner, over 10^5 events. What is the complexity, and what replaces the sort?

## A
**O(n² log n) — re-sorting inside the loop is the second classic quadratic blowup.**

Replace it with a structure that maintains order incrementally:
- only the extreme matters → `heapq` min-heap, O(log n) per update ([[cc-performance-amortized-lazy-heap]]);
- you need neighbours or a range count → keep the list sorted with `bisect.insort`;
- you need a total or a count → a running aggregate or `Counter`.

If the winner rarely changes, cache it and recompute only when the event touched it. Sorting once at the end is fine; sorting inside the loop almost never is.

## Q zh
你的代码在每个事件之后调用 `sorted(candidates)`（或对全体取 `min(...)`）来找下一个胜者，共 10^5 个事件。复杂度是多少？拿什么替掉这个排序？

## A zh
**O(n² log n) —— 循环里重排序是第二种经典的平方级爆炸。**

换成增量维护顺序的结构：
- 只关心极值 → `heapq` 最小堆，每次更新 O(log n)（[[cc-performance-amortized-lazy-heap]]）；
- 需要相邻元素或区间计数 → 用 `bisect.insort` 保持列表有序；
- 需要总和或计数 → 用增量聚合或 `Counter`。

如果胜者很少变，就把它缓存起来，只在事件触碰到它时重算。最后排一次序没问题；在循环里排序几乎总是有问题。
