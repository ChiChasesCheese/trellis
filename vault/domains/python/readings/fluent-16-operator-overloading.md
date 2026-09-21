---
nodes: [classes.operator-overloading]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 16 章 运算符重载
---
# Fluent Python 2e · 第 16 章 运算符重载

这一章讲运算符重载的规则：中缀运算符要优先支持不同类型操作数（用 `NotImplemented` 让Python 尝试反射方法），一元运算符则直接对应单个特殊方法。

**读时提取：**
- 返回 `NotImplemented`（而不是抛异常）如何触发反射方法 `__radd__` 等
- 就地运算符 `__iadd__` 与普通 `__add__` 在可变/不可变对象上的不同预期行为
- 为什么中缀运算符方法通常应该返回新对象而不是修改自身

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
