---
nodes: [model.dict-set-internals, performance.containers]
url: https://www.oreilly.com/library/view/high-performance-python/9781492055013/
tags: [book, no-archive]
title: High Performance Python 2e · 第 4 章 字典与集合
---
# High Performance Python 2e · 第 4 章 字典与集合

这一章从性能角度重讲哈希表：装载因子如何触发扩容、哈希冲突如何拖慢查找，以及为什么『用字典查表』几乎总是比『用列表线性扫描』快得多。

**读时提取：**
- 装载因子超过阈值触发扩容的代价，为什么批量插入前预估容量有意义
- 哈希冲突多的场景（如哈希函数质量差）如何退化查找性能
- 『list 里 in 判断』和『dict/set 里 in 判断』的复杂度差异

%% trellis:begin %%
## Source
[Open the original ↗](https://www.oreilly.com/library/view/high-performance-python/9781492055013/)
%% trellis:end %%
