---
nodes: [iteration.iterator-protocol, iteration.itertools]
url: https://effectivepython.com/
tags: [book, no-archive]
title: Effective Python 3e · 第 3 章 循环与迭代器
---
# Effective Python 3e · 第 3 章 循环与迭代器

这一章讲清楚 `for` 循环背后隐式调用 `iter()`/`next()`，一个迭代器耗尽后如果被第二次 `for`遍历会静默得到空结果——这是数据管道里最常见、最难查的 bug 之一；`itertools` 提供了组合这些迭代器的标准工具而不必手写状态机。

**读时提取：**
- 迭代器只能遍历一次，第二次遍历同一个迭代器对象会得到空结果而不是报错
- `enumerate`/`zip` 替代手写下标循环的场景
- `itertools.chain`/`islice`/`groupby` 各自解决什么组合问题

%% trellis:begin %%
## Source
[Open the original ↗](https://effectivepython.com/)
%% trellis:end %%
