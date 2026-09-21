---
id: generator-resumes-in-own-frame-repeatedly
node: iteration.generators
type: qa
source: cpython-internals
---
## Q
CPython 里生成器（generator）对象和普通函数调用相比，在「返回执行权给调用者」这件事上有什么本质区别？

## A
普通函数只在一次 `return` 时把执行权交还调用帧（frame），之后这次调用就结束了；生成器每次执行到一个 `yield` 表达式都会把执行权交还调用帧，但自己的帧不会被销毁，而是保留在挂起（suspended）状态。调用生成器的 `send()` 方法（`__next__()` 内部就是 `send(None)`）会让它在同一个帧里从上次挂起处继续执行，这样一次函数体可以「返回」很多次。
