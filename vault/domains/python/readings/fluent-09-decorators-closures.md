---
nodes: [functions.scope-closure, functions.decorators, functions.decorator-patterns, functions.functools]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 9 章 装饰器与闭包
---
# Fluent Python 2e · 第 9 章 装饰器与闭包

这一章先讲清楚闭包的机制——自由变量如何被内层函数“记住”，`nonlocal` 解决的是什么问题——再在此基础上讲装饰器只是“接收函数返回函数”的语法糖，以及为什么写装饰器几乎总要配 `functools.wraps`。

**读时提取：**
- 自由变量为什么在闭包里能在外层函数返回后依然存活
- `nonlocal` 要解决的具体问题：内层函数重新绑定外层变量
- 装饰器的等价写法：`@deco` 就是 `f = deco(f)`
- 忘记 `functools.wraps` 会丢失原函数的 `__name__`/`__doc__`，带来什么后果
- 带参数的装饰器为什么要多包一层函数

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
