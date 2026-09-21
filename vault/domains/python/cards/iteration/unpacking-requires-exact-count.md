---
id: unpacking-requires-exact-count
node: iteration.iterator-protocol
type: qa
source: python-docs
---
## Q
用 `a, b, c = it` 对一个迭代器做序列解包（unpacking）时，对 `it` 产出的元素个数有什么要求？

## A
必须恰好产出 3 个元素：解包本质上是反复调用 `it.__next__()` 凑够 3 个变量，然后再调用一次要求立刻得到 `StopIteration`。元素多于 3 个会抛出「too many values to unpack」的 `ValueError`，少于 3 个则抛出「not enough values to unpack」，两种情况都不会静默截断或补空。
