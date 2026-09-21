---
nodes: [iteration.generators, performance.less-ram]
url: https://www.oreilly.com/library/view/high-performance-python/9781492055013/
tags: [book, no-archive]
title: High Performance Python 2e · 第 5 章 迭代器与生成器
---
# High Performance Python 2e · 第 5 章 迭代器与生成器

这一章从内存角度讲生成器：用生成器串起数据处理管道，不需要在每一步之间物化出完整的中间列表，峰值内存能显著下降，代价是不能像列表那样重复遍历或随机访问。

**读时提取：**
- 生成器管道如何让『多步处理』不产生完整的中间列表
- 生成器换来的内存节省是以『只能遍历一次、不能随机访问』为代价的
- 什么场景下反而应该先物化成列表（比如需要多次遍历）

%% trellis:begin %%
## Source
[Open the original ↗](https://www.oreilly.com/library/view/high-performance-python/9781492055013/)
%% trellis:end %%
