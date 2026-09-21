---
nodes: [classes.pythonic-object, classes.dataclasses, classes.abc-protocols, classes.inheritance-mro]
url: https://effectivepython.com/
tags: [book, no-archive]
title: Effective Python 3e · 第 7 章 类与接口
---
# Effective Python 3e · 第 7 章 类与接口

这一章讲组合优于继承的具体判断标准：什么时候该用 mixin，什么时候该用组合加委托，并给出用 `@dataclass` 替代手写样板类、用 `collections.abc` 的抽象基类明确容器接口的建议。

**读时提取：**
- 组合（has-a）与继承（is-a）该按什么信号来选择
- mixin 类的正确用法：只提供方法，不携带独立状态
- `@dataclass` 相比手写 `__init__`/`__repr__`/`__eq__` 省下了什么

%% trellis:begin %%
## Source
[Open the original ↗](https://effectivepython.com/)
%% trellis:end %%
