---
nodes:
- runtime.stdlib-map
title: heapq 模块：堆队列算法
corpus: python-docs
section: 57-heapq
url: https://docs.python.org/3/library/heapq.html
tags:
- canonical
---

# heapq 模块：堆队列算法

heapq 把普通 list 变成一个最小堆，不是一个独立的堆类型，而是一组操作 list 的函数（heappush、heappop、heapify），堆顶（最小元素）永远是 list 的第一个元素。文档给出的典型应用包括优先级队列（用元组 priority, item 入堆，天然按 priority 排序）、以及 heapq.merge() 合并多个已排序的输入、nlargest/nsmallest 在不需要完整排序的情况下高效取 Top-K。文档特别讨论了用堆实现优先级队列时的两个实操问题：如何给同优先级的元素加一个递增序号避免比较元组时因为 item 不可比较而报错，以及如何处理任务优先级变化或任务被取消这种需要更新已入堆元素的场景（标准做法是标记旧条目为无效而不是真的从堆中删除）。这是要 Top-K 或者优先级调度时该用什么数据结构的标准答案。
