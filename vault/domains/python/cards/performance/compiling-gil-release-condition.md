---
id: compiling-gil-release-condition
node: performance.compiling
type: qa
tags: [grown]
---
## Q
NumPy 的向量化操作和用 `@numba.njit(nogil=True)` 编译的函数，在什么条件下能真正释放 GIL（全局解释器锁，Global Interpreter Lock）让其他线程并行执行？

## A
只有当这段代码从头到尾都在做纯数值计算——不创建、不引用、不操作任何 Python 对象（包括不触发引用计数变化）——才能安全释放 GIL，因为 GIL 本身保护的正是 Python 对象的引用计数和内部状态不被多线程并发破坏。哪怕函数体里只有一行涉及 Python 对象（比如往列表里追加一个元素），也无法释放 GIL，必须始终持有它。
