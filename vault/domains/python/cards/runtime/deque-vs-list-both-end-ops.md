---
id: deque-vs-list-both-end-ops
node: runtime.stdlib-map
type: qa
source: python-docs
---
## Q
需要频繁在序列两端增删元素时，为什么优先选 `collections.deque` 而不是 `list`？

## A
`deque`（双端队列）在两端做 `append`/`pop` 都是近似 O(1)，而且是线程安全的原子操作；`list` 是针对固定长度、随机访问优化的，`pop(0)`/`insert(0, v)` 这类改变列表长度和位置的操作要搬动底层数组，是 O(n)。访问模式主要是「从两头进出」时 `deque` 明显更合适；反过来 `deque` 不支持 O(1) 随机下标访问/切片，这点不如 `list`。
