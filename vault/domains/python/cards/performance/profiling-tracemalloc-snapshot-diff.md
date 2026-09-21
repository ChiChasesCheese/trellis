---
id: profiling-tracemalloc-snapshot-diff
node: performance.profiling
type: qa
source: python-docs
---
## Q
`tracemalloc` 默认每次内存分配只记录几层调用栈（frame）？为什么排查内存泄漏更该用两次快照相减（`compare_to`），而不是只看一次快照？

## A
默认只记录最近 1 层调用帧，可用 `PYTHONTRACEMALLOC=N` 或 `tracemalloc.start(N)` 提高到 N 层以定位更深的分配来源，层数越多开销越大。单次快照里混着程序启动时的大量常驻分配，用 `snapshot2.compare_to(snapshot1, 'lineno')` 看两次之间的增量才能精准定位在泄漏。
