---
id: containers-list-head-vs-deque
node: performance.containers
type: qa
source: cpython-internals
---
## Q
在 `list` 头部插入或弹出元素（`insert(0, v)` / `pop(0)`）为什么是 O(n)？要在两端频繁增删元素该用什么结构，复杂度是多少？

## A
`list` 底层是一段连续内存的指针数组，为固定长度的随机访问和尾部操作做了优化，在头部增删要把后面所有元素整体搬移一格，因此是 O(n)。需要两端都快时应该用 `collections.deque`（双端队列），它两端的 `append`/`appendleft`/`pop`/`popleft` 都近似 O(1)。
