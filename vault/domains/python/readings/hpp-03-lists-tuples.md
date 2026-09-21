---
nodes: [performance.containers, model.sequences]
url: https://www.oreilly.com/library/view/high-performance-python/9781492055013/
tags: [book, no-archive]
title: High Performance Python 2e · 第 3 章 列表与元组
---
# High Performance Python 2e · 第 3 章 列表与元组

这一章从底层实现讲 `list`（可变、过量分配以摊销 append 成本）和 `tuple`（不可变、更紧凑）在内存布局和操作耗时上的差异，以及为什么该用对容器而不是靠『都差不多』的直觉。

**读时提取：**
- `list` 的过量分配（over-allocation）如何让 `append` 均摊 O(1)
- `tuple` 因为不可变，在创建和小对象缓存上比 `list` 更省
- 在头部频繁插入/删除时为什么 `list` 不是好选择，`deque` 才是

%% trellis:begin %%
## Source
[Open the original ↗](https://www.oreilly.com/library/view/high-performance-python/9781492055013/)
%% trellis:end %%
