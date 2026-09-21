---
nodes: [iteration.generators, iteration.yield-from]
url: https://effectivepython.com/
tags: [book, no-archive]
title: Effective Python 3e · 第 6 章 推导式与生成器
---
# Effective Python 3e · 第 6 章 推导式与生成器

这一章讲当推导式变得太复杂（嵌套、多个 if）时该换成生成器函数，以及生成器如何用惰性求值避免一次性把整个中间结果放进内存，这对处理大数据流尤其重要。

**读时提取：**
- 多层嵌套推导式何时应该拆成显式的生成器函数以保住可读性
- 生成器的惰性求值如何避免中间列表占用内存
- `yield from` 委托子生成器时如何保留原有的返回值语义

%% trellis:begin %%
## Source
[Open the original ↗](https://effectivepython.com/)
%% trellis:end %%
