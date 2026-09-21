---
nodes: [iteration.context-managers, iteration.comprehensions]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 18 章 with、match 与 else 语句块
---
# Fluent Python 2e · 第 18 章 with、match 与 else 语句块

这一章讲上下文管理器协议（`__enter__`/`__exit__`）如何让 `with` 保证资源释放，`match` 语句的结构化模式匹配能拆解序列/映射/对象，以及 `for...else`/`while...else` 里的 `else` 只在循环正常结束（没有 `break`）时执行。

**读时提取：**
- `__exit__` 返回 True 会吞掉异常，这个细节容易被忽略
- `contextlib.contextmanager` 如何用一个生成器函数写出上下文管理器
- `match` 语句的模式可以解构序列、字典、对象属性，不只是匹配字面量
- `for...else` 的 `else` 只在循环没有被 `break` 中断时执行

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
