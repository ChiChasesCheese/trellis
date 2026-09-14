---
id: cc-toolbox-sorted-range-count
node: toolbox.sorted
type: qa
---
## Q
A sorted list of timestamps and thousands of queries "how many events in `[lo, hi]`, both ends inclusive". Cost per query?

## A
**O(log n) with two bisections:** `bisect_right(a, hi) - bisect_left(a, lo)`.

- Inclusive `lo` needs `bisect_left` (first `>= lo`); inclusive `hi` needs `bisect_right` (first `> hi`). Getting either backwards silently drops or double-counts the boundary elements — and boundary elements are exactly what the hidden tests place there.
- Half-open `[lo, hi)` is `bisect_left(a, hi) - bisect_left(a, lo)`.
- `bisect` accepts `key=` from Python 3.10; on an older runtime keep a parallel list of the keys and bisect that instead of building tuples.
- If the query is a **sum** rather than a count, pair the sorted list with a prefix-sum array and subtract two prefix values ([[cc-algorithms-prefix-range-query]]).

## Q zh
一个有序时间戳列表和上千个查询「`[lo, hi]` 内有多少事件，两端都闭」。每次查询的代价？

## A zh
**两次二分，O(log n)：** `bisect_right(a, hi) - bisect_left(a, lo)`。

- 左端闭需要 `bisect_left`（第一个 `>= lo`）；右端闭需要 `bisect_right`（第一个 `> hi`）。任何一边搞反都会静默地漏掉或重复计入边界元素 —— 而边界元素正是隐藏测试特意放在那里的。
- 半开区间 `[lo, hi)` 是 `bisect_left(a, hi) - bisect_left(a, lo)`。
- Python 3.10 起 `bisect` 支持 `key=`；在更老的运行时里，维护一个平行的 key 列表去二分，而不是构造 tuple。
- 如果查询要的是**和**而不是计数，就给有序列表配一个前缀和数组，相减两个前缀值（[[cc-algorithms-prefix-range-query]]）。
