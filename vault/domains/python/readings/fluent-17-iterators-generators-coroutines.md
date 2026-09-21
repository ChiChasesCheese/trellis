---
nodes: [iteration.iterator-protocol, iteration.generators, iteration.yield-from]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 17 章 迭代器、生成器与经典协程
---
# Fluent Python 2e · 第 17 章 迭代器、生成器与经典协程

这一章把可迭代对象（实现 `__iter__`）和迭代器（实现 `__iter__` 和 `__next__`）分开讲，再讲生成器函数如何用 `yield` 自动实现这套协议，以及 `yield from` 如何把子生成器的值和`StopIteration` 的返回值透明地转发出去。

**读时提取：**
- 可迭代对象与迭代器的区别：前者能反复 `iter()`，后者是一次性的游标
- 生成器函数调用后不立即执行，第一次 `next()` 才跑到第一个 `yield`
- `yield from` 如何转发子生成器的值、异常和最终返回值
- 经典协程（用 `yield` 接收 `send()` 的值）和后来 `async`/`await` 协程的关系

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
