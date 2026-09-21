---
nodes:
- runtime.adaptive-jit
- runtime.frames-eval
title: 字节码解释器：栈机、调用栈重构与自适应特化
corpus: cpython-internals
section: 008-the-bytecode-interpreter
url: https://github.com/python/cpython/blob/main/InternalDocs/interpreter.md
tags:
- canonical
---

# 字节码解释器：栈机、调用栈重构与自适应特化

这是理解“解释器循环”本身的核心文档：CPython 的解释器是一台栈机，每条指令从求值栈上弹出/压入对象；3.11 起 Python 调用 Python 不再递归进 C 函数栈（避免 C 栈溢出风险），而是把新帧压进解释器自己维护的调用栈、直接跳转到被调函数的字节码开头，返回时再跳回去，省掉大量 C 栈开销。文档后半部分讲“特化”（specialization）：像 `LOAD_GLOBAL` 这类通用指令执行到一定次数后，会用内联缓存里记录的运行时信息把自己替换成 `LOAD_GLOBAL_MODULE`/`LOAD_GLOBAL_BUILTIN` 这类针对具体情况优化过的快指令，一旦假设不成立就退化回通用版本。读完能把“3.11+ 自适应解释器按类型内联快速路径”这句话具体化成“为什么、怎么内联、什么时候会退化”，是回答“Python 到底慢在哪、3.11 做了什么”的第一手材料。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/python/cpython/blob/main/InternalDocs/interpreter.md)

## Archived copy
![[cpy-bytecode-interpreter-clip]]
%% trellis:end %%
