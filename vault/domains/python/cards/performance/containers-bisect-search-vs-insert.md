---
id: containers-bisect-search-vs-insert
node: performance.containers
type: qa
source: cpython-internals
---
## Q
`bisect` 模块能在 O(log n) 内找到有序列表的插入点，为什么 `bisect.insort()` 整体仍然是 O(n)，而不是 O(log n)？

## A
`bisect_left`/`bisect_right` 只做二分查找，确实是 O(log n)；但 `insort()` 找到插入点后要调用 `list.insert()` 把插入点右边的所有元素整体搬移一格腾出空间，这一步是 O(n) 且主导了总耗时，所以二分查找带来的优势被插入本身吃掉了。
