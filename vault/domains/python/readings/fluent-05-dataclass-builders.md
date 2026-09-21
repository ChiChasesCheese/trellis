---
nodes: [classes.dataclasses]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 5 章 数据类构造器
---
# Fluent Python 2e · 第 5 章 数据类构造器

这一章对比 `namedtuple`、`typing.NamedTuple`、`@dataclass` 三种“数据类构造器”，它们都在减少手写 `__init__`/`__repr__`/`__eq__` 的样板代码，但在可变性、默认值、继承上行为不同。

**读时提取：**
- 三种构造器在“是否可变”“是否支持默认值/类型注解”上的差异
- `@dataclass(frozen=True)` 和 `eq=True` 分别改变了什么
- 什么时候数据类不够用，需要退回到手写的普通类

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
