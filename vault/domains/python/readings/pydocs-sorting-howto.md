---
nodes:
- performance.containers
title: 排序技巧（Sorting Techniques）
corpus: python-docs
section: 09-sorting
url: https://docs.python.org/3/howto/sorting.html
tags:
- canonical
---

# 排序技巧（Sorting Techniques）

这篇 HOWTO 系统讲解 list.sort() 和 sorted() 的实战用法：用 key= 参数而不是自定义比较函数（更快也更清晰）、用 operator.itemgetter/attrgetter 代替 lambda 提升性能、如何组合多个排序键实现多级排序，以及最重要的一点，Python 的排序算法（Timsort）是稳定的，相同键的元素会保持原有的相对顺序，这让先按 A 排序再按 B 排序这种多级排序技巧成立。文中还讲了旧式比较函数（cmp 风格）如何通过 functools.cmp_to_key 转换成 key 函数以兼容现代 API，以及面对不可比较类型（如 None 和 int 混排）该怎么处理。读完能说清为什么 Python 排序默认稳定以及如何利用这一点写出正确的多级排序，而不需要自己实现排序算法。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/howto/sorting.html)

## Archived copy
![[pydocs-sorting-howto-clip]]
%% trellis:end %%
