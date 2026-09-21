---
nodes:
- concurrency.free-threading
- memory.interning-immortal
title: 自由线程 Python（无 GIL 构建）
corpus: python-docs
section: 07-free-threading-python
url: https://docs.python.org/3/howto/free-threading-python.html
tags:
- canonical
---

# 自由线程 Python（无 GIL 构建）

3.13 起 CPython 提供了可选的自由线程构建（--disable-gil），真正去掉了 GIL，让多线程可以并行执行 Python 字节码。这篇文档讲清了代价：单线程性能有约 1-8% 的开销（因为改用偏向引用计数和逐对象锁替代了 GIL 的粗粒度保护）；C 扩展如果没有针对性适配可能不兼容；帧对象、迭代器等原本隐式线程安全的东西现在需要显式加锁。文中特别提到不朽对象（immortal objects，如 None/True/小整数）在自由线程下如何避免引用计数的写竞争，这是 3.12 引入、3.13 起发挥关键作用的优化。面试被问到 Python 会不会去掉 GIL 时，这篇文档给出的是官方现状而不是道听途说：目前是可选构建，不是默认行为，生态兼容性仍在推进中。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/howto/free-threading-python.html)

## Archived copy
![[pydocs-free-threading-clip]]
%% trellis:end %%
