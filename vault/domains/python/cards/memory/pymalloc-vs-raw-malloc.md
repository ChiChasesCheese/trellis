---
id: pymalloc-vs-raw-malloc
node: memory.allocator
type: qa
tags: [grown]
source: python-docs
---
## Q
既然操作系统和 C 标准库已经提供了通用的 `malloc`/`free`，CPython 为什么还要在它上面再实现一层 pymalloc？

## A
Python 程序会非常频繁地创建和销毁大量体积很小的对象（小整数、短字符串、小 tuple 等），而通用 `malloc` 面向任意大小设计，每次调用都有加锁、元数据记账等固定开销，对小分配来说这部分开销占比很高。pymalloc 用相同大小的 block 分组池化、按需从预先申请好的 arena 里切出 pool，为「大量同型小对象」的场景把这部分固定开销摊薄，分配和释放都比直接调用系统 `malloc` 快。
