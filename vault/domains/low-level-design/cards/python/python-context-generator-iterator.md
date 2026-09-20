---
id: python-context-generator-iterator
node: python.context-iterators
type: qa
step: 4
tags: [grown]
---
## Q
一个用 `yield` 写的生成器函数为什么能直接当迭代器（iterator）用，不用手写一个带 `__iter__`/`__next__` 的类？

## A
调用生成器函数不会立刻执行函数体，而是返回一个**生成器对象**，这个对象自动实现了 `__iter__`（返回自己）和 `__next__`（从上次 `yield` 处恢复，跑到下一个 `yield` 或函数结束抛 `StopIteration`）——Python 帮你把“记住当前遍历到哪、下次调用从哪继续”这套状态机全部生成好了，代价是你只写线性的、顺着读的代码，不用手动维护游标字段。
