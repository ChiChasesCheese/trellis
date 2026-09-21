---
nodes: [model.dunder-protocols, model.sequences]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 12 章 序列的特殊方法
---
# Fluent Python 2e · 第 12 章 序列的特殊方法

这一章通过实现一个自定义向量类，展示切片、拼接、原地运算这些行为背后分别对应哪个特殊方法，以及为什么支持切片需要正确处理 `slice` 对象而不是只处理单个索引。

**读时提取：**
- `__getitem__` 收到 `slice` 对象时该如何正确返回同类型的切片
- `__len__`/`__iter__`/`__contains__` 之间的默认实现关系
- 就地运算符（`+=`）对应 `__iadd__`，缺失时如何回退到 `__add__`

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
