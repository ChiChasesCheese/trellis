---
nodes: [classes.properties-descriptors]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 23 章 属性描述符
---
# Fluent Python 2e · 第 23 章 属性描述符

这一章讲描述符协议（`__get__`/`__set__`/`__delete__`）是 `property`、`classmethod`、`staticmethod` 背后的统一机制，理解它才能自己写出可复用的『带校验的字段』而不是每个类都重写 property。

**读时提取：**
- 描述符分『数据描述符』（同时有 `__get__`/`__set__`）和『非数据描述符』，优先级不同
- `property` 本质上就是一个内置的数据描述符
- 描述符实例通常定义在类属性上，被所有实例共享，状态该存在哪里要想清楚

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
