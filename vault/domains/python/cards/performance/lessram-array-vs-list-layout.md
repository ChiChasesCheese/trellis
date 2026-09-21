---
id: lessram-array-vs-list-layout
node: performance.less-ram
type: qa
source: python-docs
---
## Q
存储一百万个整数时，用 `array.array('q', ...)` 和用普通 `list` 在内存布局上有什么本质区别？

## A
`list` 存的是一百万个指向 Python `int` 对象的指针，每个 `int` 对象自己还带引用计数、类型指针等对象头部开销；`array('q', ...)` 按 C 的 signed long long（8 字节）把原始数值紧凑连续存放，没有对象头部，也不用为每个元素单独分配堆内存，单元大小由 `itemsize` 属性给出，存同质数值时比 list 省得多。
