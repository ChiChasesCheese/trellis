---
nodes:
- asyncio.contextvars
title: PEP 567：上下文变量（contextvars）
corpus: peps
section: 25-pep-0567
url: https://peps.python.org/pep-0567/
tags:
- canonical
---

# PEP 567：上下文变量（contextvars）

PEP 567 解释了为什么 `threading.local` 在异步代码里是错的：一个线程上交替运行着许多 Task，线程局部存储会让不同请求互相污染。它定义了 `ContextVar`、不可变的 `Context` 映射与 `copy_context()`：asyncio 在创建每个 Task 时复制当前上下文，之后 Task 内对变量的 `set()` 只影响自己那份，`await` 之间自然隔离。读时抓住三个机制：Context 是写时复制的不可变映射（HAMT），所以复制是 O(1)；`Token` 让 `reset()` 精确回滚；`decimal` 模块的精度上下文正是第一个迁移到 contextvars 的标准库用户。面试里由此能回答「追踪 ID 怎么跨 await 传播」与「为什么 gather 里各协程看到的上下文一样」。

%% trellis:begin %%
## Source
[Open the original ↗](https://peps.python.org/pep-0567/)

## Archived copy
![[peps-context-variables-clip]]
%% trellis:end %%
