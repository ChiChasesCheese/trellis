---
nodes:
- concurrency.free-threading
title: PEP 734：标准库中的多解释器（Multiple Interpreters）
corpus: peps
section: 02-pep-0734
url: https://peps.python.org/pep-0734/
tags:
- canonical
---

# PEP 734：标准库中的多解释器（Multiple Interpreters）

补上“除了线程和进程还有第三条并行路径”这一常被面试者忽略的选项：子解释器（subinterpreter）。文档先讲清楚线程状态（PyThreadState）与解释器状态（PyInterpreterState）的一对多关系，再说明 CPython 的子解释器彼此严格隔离——不共享 sys.modules、类、函数，甚至同名类也各有一份，只有不可变的内建单例（None、小整数）才共享。这解决了什么：per-interpreter GIL（PEP 684）让每个子解释器有自己的 GIL，从而在同一进程内获得真并行，同时避免了多进程方案的 fork/pickle 开销和 CUDA 上下文冲突。动机部分点明这是把长期只有 C API 才能用的能力，通过新的 interpreters 模块和 InterpreterPoolExecutor 开放给纯 Python 代码。面试追问“子解释器和多进程有什么本质区别”时，隔离边界和共享内存的取舍就是答案。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-0734/)

## Archived copy
![[peps-pep734-subinterpreters-clip]]
%% trellis:end %%
