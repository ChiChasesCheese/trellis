---
id: genexp-lazy-vs-listcomp-materialize
node: iteration.generators
type: qa
source: cpython-internals
---
## Q
`(x for x in seq)`（生成器表达式）和 `[x for x in seq]`（列表推导）在内存占用上的根本区别是什么？为什么处理无限流或超大数据时要选前者？

## A
列表推导会立刻把所有结果计算出来、物化（materialize）成一个完整的 list，内存占用正比于元素个数；生成器表达式返回的是一个生成器（惰性迭代器），只在被 `next()` 驱动时才计算下一个值，任意时刻只保留当前这一步需要的状态，内存占用是 O(1)。如果数据源是无限流或体积远超内存，列表推导会耗尽内存甚至永远算不完，只有生成器表达式可用。
