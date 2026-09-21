---
id: infinite-iterator-max-min-in-hangs
node: iteration.iterator-protocol
type: qa
source: python-docs
---
## Q
为什么对一个无限（infinite，永不抛出 `StopIteration`）的迭代器调用 `max()`、`min()`，或用 `in` 查找一个不存在的元素，会是危险操作？

## A
这些操作内部都要反复调用 `__next__()` 直到遇到 `StopIteration` 才能给出结论：`max`/`min` 要看遍全部元素才能确定最值，`in` 要么命中目标要么耗尽整个流才能返回 False。如果迭代器永远产出新元素且目标值从不出现，调用会一直阻塞、永不返回，程序表现为挂死。
