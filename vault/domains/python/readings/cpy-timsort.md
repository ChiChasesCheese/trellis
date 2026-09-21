---
nodes:
- performance.containers
title: Timsort：为什么 list.sort() 对“已经有点顺序”的数据特别快
corpus: cpython-internals
section: 015-list-sort-algorithm-timsort
url: https://github.com/python/cpython/tree/main/InternalDocs
tags:
- canonical
---

# Timsort：为什么 list.sort() 对“已经有点顺序”的数据特别快

Timsort 先从左到右识别天然存在的升序/降序片段（run），太短的话用二分插入排序把它补到 `minrun` 长度，再两两归并相邻的 run。关键的自适应设计有两处：一是用“powersort”策略决定先合并哪两个 run，保证归并树尽量平衡，为了稳定性永远只合并相邻的两个 run（不能跳着合并，否则会打乱相同元素的原始相对顺序）；二是“galloping”模式——当某个 run 连续赢了好几轮比较，就切换成指数查找去一次性搬一大块，把比较次数从 O(n) 降到 O(log n)，代价是在真正随机的数据上会略微多做一点无用功，所以有 `min_gallop` 动态调节要不要保持这个模式。读完能把“Timsort 稳定且利用已有序段”这句结论具体化：面试被追问“为什么快”“最坏情况是多少”时能讲出 run/merge/gallop 这条机制链，而不只是背“它是归并和插入排序的混合体”。
