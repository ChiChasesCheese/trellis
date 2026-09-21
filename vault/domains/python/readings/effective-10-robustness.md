---
nodes: [runtime.exceptions, engineering.robustness, iteration.context-managers]
url: https://effectivepython.com/
tags: [book, no-archive]
title: Effective Python 3e · 第 10 章 健壮性
---
# Effective Python 3e · 第 10 章 健壮性

这一章讲防御式编程的具体做法：`try`/`except`/`else`/`finally` 各自的执行时机、自定义异常类层次如何让调用方能分级处理错误，以及 `contextlib` 如何保证清理代码总会执行。

**读时提取：**
- `try`/`except`/`else`/`finally` 四块各自在什么条件下执行
- 自定义异常层次结构如何让调用方按粒度捕获错误
- `contextlib.closing`/`suppress` 等工具解决的具体清理场景

%% trellis:begin %%
## Source
[Open the original ↗](https://effectivepython.com/)
%% trellis:end %%
