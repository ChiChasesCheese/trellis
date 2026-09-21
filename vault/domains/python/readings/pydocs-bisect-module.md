---
nodes:
- runtime.stdlib-map
title: bisect 模块：有序数组二分查找
corpus: python-docs
section: 58-bisect
url: https://docs.python.org/3/library/bisect.html
tags:
- canonical
---

# bisect 模块：有序数组二分查找

bisect 提供了在已排序列表里做二分查找和二分插入的函数：bisect_left/bisect_right 返回该插入的位置（区别在于遇到相等元素时插在左边还是右边），insort_left/insort_right 直接完成插入并保持列表有序。文档强调这些函数只在输入列表本身已经有序的前提下才有意义，对无序列表调用不会报错但结果没有意义。典型应用包括用一组阈值给数值分级（比如按分数划分等级）、维护一个动态更新还要保持有序的列表（比如排行榜插入新分数）。文档还给出了性能提示：反复调用 insort 维护一个大列表有序，插入本身是 O(n)（要搬移元素），如果频繁插入删除，heapq 或平衡树结构可能更合适，bisect 更适合插入不频繁、查找频繁的场景。
