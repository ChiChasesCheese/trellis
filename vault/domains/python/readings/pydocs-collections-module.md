---
nodes:
- runtime.stdlib-map
- performance.containers
title: collections 模块：专用容器数据类型
corpus: python-docs
section: 48-collections
url: https://docs.python.org/3/library/collections.html
tags:
- canonical
---

# collections 模块：专用容器数据类型

collections 模块提供了一组比内建 list/dict 更专用、性能特征更明确的容器：deque 在两端插入/删除都是 O(1)（普通 list 在头部插入是 O(n)，需要搬移全部元素），是实现队列、滑动窗口的首选；Counter 是专为计数设计的字典子类，most_common(n) 一步拿到出现次数最多的元素；defaultdict 通过工厂函数自动填充缺失键的默认值，省去每次访问前判断键是否存在；namedtuple 让元组的每个位置有了名字，兼顾了元组的轻量和可读性；ChainMap 把多个字典串成一个视图，常用来实现局部配置覆盖全局配置的查找链。这些数据结构各自解决一个具体的性能或表达力问题，选对容器往往比优化算法本身收益更大，是容器选型时该第一时间想到的工具箱。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/collections.html)

## Archived copy
![[pydocs-collections-module-clip]]
%% trellis:end %%
