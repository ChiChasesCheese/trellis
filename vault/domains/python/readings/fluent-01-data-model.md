---
nodes: [model.dunder-protocols, classes.pythonic-object]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 1 章 Python 数据模型
---
# Fluent Python 2e · 第 1 章 Python 数据模型

这一章讲的是 Python 里“一致性”的来源：`len()`、`[]`、`for`、`+` 这些看起来是语法的东西，背后都是解释器在按约定调用对象的特殊方法（dunder methods）。理解这套协议，才能看懂为什么自定义对象只要实现几个特殊方法就能像内置类型一样被切片、迭代、比较。

**读时提取：**
- 数据模型是一套由解释器调用的协议，不是继承出来的接口
- `__len__`、`__getitem__` 等特殊方法如何让自定义类支持内置语法
- 为什么这套协议让第三方对象和内置对象在使用体验上没有区别

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
