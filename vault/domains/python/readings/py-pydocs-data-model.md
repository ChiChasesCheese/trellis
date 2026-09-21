---
nodes:
- model.names-objects
- model.mutability
- model.numbers
- model.sequences
- model.dunder-protocols
- model.hash-eq
- classes.operator-overloading
- iteration.context-managers
- memory.refcounting
- classes.metaprogramming
title: 数据模型（Data Model）参考
corpus: python-docs
section: 01-datamodel
url: https://docs.python.org/3/reference/datamodel.html
tags:
- canonical
---

# 数据模型（Data Model）参考

这是 Python 官方参考手册中最核心的一章，定义了整个对象系统的底层规则：每个对象都有身份（identity）、类型（type）、值（value）三要素，`is` 比较身份而 `==` 调用 `__eq__` 比较值；可变对象与不可变对象的区别决定了别名与副作用；数值、序列、映射等内建类型如何归入统一的类型层级；对象在引用计数归零时立即释放，但循环引用需要额外的垃圾回收器处理。第 3.3 节逐一列出解释器通过哪些特殊方法（dunder）实现 repr、比较运算符、算术运算符与 with 语句，并明确规定 `__eq__` 与 `__hash__` 必须保持一致；`__init_subclass__` 和 `__set_name__` 这两个钩子让多数"需要元类"的场景（注册子类、拿到属性名）不用真的写元类就能实现。这不是一篇教程，而是权威定义，遇到"这个行为到底该不该这样"的疑问时应回来查这里，而不是凭直觉猜测。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/reference/datamodel.html)

## Archived copy
![[py-pydocs-data-model-clip]]
%% trellis:end %%
