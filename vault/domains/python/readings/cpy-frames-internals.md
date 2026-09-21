---
nodes:
- runtime.frames-eval
title: 帧（Frame）的内存布局与 3.11 的惰性创建优化
corpus: cpython-internals
section: 007-frames
url: https://github.com/python/cpython/blob/main/InternalDocs/frames.md
tags:
- canonical
---

# 帧（Frame）的内存布局与 3.11 的惰性创建优化

每次函数调用的“活动记录”——局部变量、求值栈、以及全局字典/代码对象等元信息——统称一个帧。3.11 之前每次调用都要在堆上分配一个 `PyFrameObject`，开销不小；3.11 起帧被拆成轻量的 `_PyInterpreterFrame`，绝大多数情况下连续分配在每线程私有的栈上（类似 C 的调用栈），只有当 Python 代码真的用到 `sys._getframe()`、或者要生成 traceback 时，才会临时创建出一个货真价实的 `PyFrameObject` 并把内容拷过去——这就是“帧对象的惰性创建”。生成器/协程是特例：它们的帧直接嵌在生成器对象里，不走每线程栈。读这篇能解释递归为什么会撞 `sys.setrecursionlimit`（每层调用都要占一份帧空间）、以及为什么 3.11 之后函数调用明显变快（省掉了大部分堆分配）。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/python/cpython/blob/main/InternalDocs/frames.md)

## Archived copy
![[cpy-frames-internals-clip]]
%% trellis:end %%
