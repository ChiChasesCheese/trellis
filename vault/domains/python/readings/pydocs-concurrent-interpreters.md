---
nodes:
- concurrency.free-threading
title: concurrent.interpreters：子解释器提供的另一条多核路径
corpus: python-docs
section: 27-concurrent-interpreters
url: https://docs.python.org/3/library/concurrent.interpreters.html
tags:
- canonical
---

# concurrent.interpreters：子解释器提供的另一条多核路径

3.14 新增的 concurrent.interpreters 模块暴露了 CPython 长期存在但此前只能通过 C API 使用的子解释器（subinterpreter）能力：在同一个进程里跑多个互相隔离的解释器实例，每个都有自己的 sys.modules 和全局状态，彼此不共享内存（除非显式通过专门的通信原语传递数据）。这和多进程类似，都是靠隔离换并行，但子解释器比进程轻量得多，创建和切换的开销更小。文档明确指出子解释器之间的通信需要用专门设计的 API（类似跨进程通信但更受限），不能像多线程那样直接共享 Python 对象。这是除了多线程（受 GIL 限制）、多进程（重）、自由线程构建（还在推广期）之外，Python 应对多核的第四条路径，面试聊 Python 的并发/并行选项时提到这个会显得对生态现状很了解。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/concurrent.interpreters.html)

## Archived copy
![[pydocs-concurrent-interpreters-clip]]
%% trellis:end %%
