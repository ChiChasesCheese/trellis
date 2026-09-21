---
nodes: [classes.inheritance-mro]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 14 章 继承：为了更好或更坏
---
# Fluent Python 2e · 第 14 章 继承：为了更好或更坏

这一章讲清楚 Python 用 C3 线性化算法计算方法解析顺序（MRO），`super()` 沿着这条顺序走而不是沿着字面上的父类走，这也是多重继承和 mixin 能协作的关键；同时警告继承内置类型（如 `dict`）容易出现方法不一致地调用到 C 实现的坑。

**读时提取：**
- MRO 由 C3 线性化算法计算，`super()` 按 MRO 顺序查找而非直接找父类
- mixin 类为什么依赖『下一个在 MRO 里的类』这种约定而不是显式父类
- 直接继承内置类型（如 `dict`/`list`）时方法覆盖不生效的坑
- 多重继承时该如何设计 mixin 顺序，避免 MRO 冲突

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
