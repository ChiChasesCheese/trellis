---
nodes: [classes.pythonic-object]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 11 章 符合 Python 风格的对象
---
# Fluent Python 2e · 第 11 章 符合 Python 风格的对象

这一章综合示范一个“地道”的 Python 类要实现哪些特殊方法：`__repr__`、`__eq__`、`__hash__`、`__format__`、备选构造器 `classmethod`，把前面几章的协议串成一个完整对象。

**读时提取：**
- `__repr__` 面向开发者、`__str__` 面向终端用户，两者该怎么分工
- 实现 `__eq__` 之后为什么经常要一并处理 `__hash__`（或显式设为不可哈希）
- `classmethod` 作为备选构造器（如 `from_bytes`）的典型用法

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
