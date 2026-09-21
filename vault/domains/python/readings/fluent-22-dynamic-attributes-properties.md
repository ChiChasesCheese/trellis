---
nodes: [classes.attribute-lookup, classes.properties-descriptors]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 22 章 动态属性与特性
---
# Fluent Python 2e · 第 22 章 动态属性与特性

这一章讲 `__getattr__`/`__setattr__` 如何拦截属性访问实现动态属性，以及 `property` 如何把『看起来是属性访问』的代码悄悄变成方法调用，从而在不改调用方代码的前提下加校验或惰性计算。

**读时提取：**
- `__getattr__`（找不到才调用）与 `__getattribute__`（每次都调用）的区别
- `property` 让 getter/setter 看起来像普通属性访问，方便后续加校验而不破坏调用方
- 动态属性访问失控时如何用 `__slots__` 或显式属性名单收紧

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
