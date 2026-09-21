---
id: refcount-deterministic-vs-gc
node: memory.refcounting
type: qa
source: cpython-internals
---
## Q
为什么说 CPython 的引用计数（reference count）回收是「确定性」的，而循环垃圾回收（cyclic GC）不是？

## A
引用计数在某个对象的计数减到 0 的那一刻就立即释放它，释放时机可以从代码逻辑直接推断；循环 GC 只在某一代（generation）的分配/回收次数超过阈值时才触发扫描，触发时机不可预测。对象的 `__del__` 之所以能在 `del` 后立刻执行，靠的正是引用计数归零，而不是循环 GC。
