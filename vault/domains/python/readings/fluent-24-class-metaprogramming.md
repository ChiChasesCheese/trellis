---
nodes: [classes.metaprogramming]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 24 章 类元编程
---
# Fluent Python 2e · 第 24 章 类元编程

这一章讲类本身也是对象（`type` 的实例），元类可以在类创建时介入、改写它的命名空间和方法，`__init_subclass__` 和类装饰器则是更轻量、更常用的替代方案，能覆盖大多数元类的使用场景。

**读时提取：**
- 类是 `type` 的实例，`type(name, bases, ns)` 就是创建类的底层方式
- 元类通过重写 `__new__`/`__init__` 在类创建时介入，早于任何实例存在
- `__init_subclass__` 和类装饰器为什么常常是比自定义元类更简单的选择

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
