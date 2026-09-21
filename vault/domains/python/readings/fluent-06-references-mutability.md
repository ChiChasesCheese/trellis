---
nodes: [model.names-objects, model.mutability, model.copy, memory.refcounting, memory.weakref]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 6 章 对象引用、可变性与垃圾回收
---
# Fluent Python 2e · 第 6 章 对象引用、可变性与垃圾回收

这一章纠正“变量是盒子”的直觉：Python 变量是贴在对象上的标签（name → object），赋值是重新贴标签而不是拷贝值；这解释了默认可变参数的经典坑、浅拷贝与深拷贝的区别，以及引用计数为何是 CPython 回收对象的第一道机制。

**读时提取：**
- “变量是标签，不是盒子”如何解释别名（aliasing）导致的意外共享
- 浅拷贝、深拷贝、`copy.copy`/`copy.deepcopy` 的边界
- 函数默认参数只求值一次，为什么可变默认值是经典陷阱
- 引用计数归零即释放，`weakref` 如何在不增加引用计数的前提下持有对象

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
