---
nodes: [runtime.stdlib-map, engineering.money-time, engineering.serialization, performance.containers]
url: https://effectivepython.com/
tags: [book, no-archive]
title: Effective Python 3e · 第 12 章 数据结构与算法
---
# Effective Python 3e · 第 12 章 数据结构与算法

这一章过一遍标准库里『不用自己实现』的数据结构（`heapq`、`bisect`、`collections` 系列）和它们各自的复杂度特征，以及 `decimal`/`datetime` 这类『看起来简单但精度和时区容易出错』的内置类型，还有序列化格式的取舍。

**读时提取：**
- `heapq` 实现优先队列、`bisect` 维护有序列表插入点，分别对应什么复杂度
- 为什么涉及金额计算要用 `decimal.Decimal` 而不是 `float`
- `pickle`/`json` 在安全性、跨语言兼容性上的取舍

%% trellis:begin %%
## Source
[Open the original ↗](https://effectivepython.com/)
%% trellis:end %%
