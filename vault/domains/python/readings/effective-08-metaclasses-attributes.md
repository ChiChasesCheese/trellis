---
nodes: [classes.attribute-lookup, classes.properties-descriptors, classes.metaprogramming]
url: https://effectivepython.com/
tags: [book, no-archive]
title: Effective Python 3e · 第 8 章 元类与属性
---
# Effective Python 3e · 第 8 章 元类与属性

这一章的立场是：`property`、描述符、`__init_subclass__`、类装饰器能覆盖绝大多数需求，自定义元类应该是最后手段，因为它改变了类创建本身，调试和可读性成本都更高。

**读时提取：**
- `property` 用来在不破坏调用方代码的前提下给字段加校验或惰性计算
- `__init_subclass__` 如何在子类定义时做检查，且比元类更容易读懂
- 什么信号说明真的需要自定义元类，而不是上面两种更轻的手段

%% trellis:begin %%
## Source
[Open the original ↗](https://effectivepython.com/)
%% trellis:end %%
