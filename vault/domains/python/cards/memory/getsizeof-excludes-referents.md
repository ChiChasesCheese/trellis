---
id: getsizeof-excludes-referents
node: memory.object-size
type: qa
source: cpython-internals
---
## Q
`sys.getsizeof(obj)` 返回的字节数，包含 `obj` 所引用的其他对象占用的内存吗？

## A
不包含。`getsizeof()` 只统计直接属于这个对象本身的内存（通过调用对象的 `__sizeof__` 方法得到，如果这个对象受垃圾回收器（garbage collector）管理还会加上 GC 记账用的额外开销），不会递归统计它引用的其他对象；要得到一个容器连同其内容的总内存，需要自己写递归遍历去累加。
