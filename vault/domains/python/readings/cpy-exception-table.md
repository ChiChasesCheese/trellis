---
nodes:
- runtime.exceptions
title: 零成本异常处理：try 不抛异常时到底付了多少代价
corpus: cpython-internals
section: 011-exception-handling
url: https://github.com/python/cpython/blob/main/InternalDocs/exception_handling.md
tags:
- canonical
---

# 零成本异常处理：try 不抛异常时到底付了多少代价

Python 的异常处理是“零成本”的：`try`/`except` 编译后并不会插入运行时判断，`SETUP_FINALLY`/`POP_BLOCK` 这类伪指令在生成最终字节码时会被整体删掉，取而代之的是一张单独存在代码对象里的“异常表”（`co_exceptiontable`），把每个指令区间映射到覆盖它的异常处理器、以及处理器期望的求值栈深度。只有真的抛出异常时，解释器才去查这张表（用紧凑的变长编码存储，支持二分查找），把栈弹到匹配深度、跳到处理器继续执行——没有异常发生时完全不产生额外开销。文档也讲了隐式链式异常 `__context__` 和显式 `raise ... from` 对应的 `__cause__` 分别在哪里被设置。读完能把“try 块本身几乎不花钱，只有真抛异常才花钱”这个直觉背后的机制讲清楚，对应到面试里“异常控制流成本”这类追问。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/python/cpython/blob/main/InternalDocs/exception_handling.md)

## Archived copy
![[cpy-exception-table-clip]]
%% trellis:end %%
