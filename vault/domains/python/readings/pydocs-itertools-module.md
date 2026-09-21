---
nodes:
- iteration.itertools
title: itertools 模块：惰性迭代器工具
corpus: python-docs
section: 45-itertools
url: https://docs.python.org/3/library/itertools.html
tags:
- canonical
---

# itertools 模块：惰性迭代器工具

itertools 提供的函数全部返回惰性迭代器，可以自由组合成处理流水线而不需要在中间步骤把数据物化成完整列表，这对处理大数据流或无限序列（如 itertools.count()）至关重要。文档把函数分成几类：创建新迭代器（chain、cycle、repeat）、按元素处理（starmap、accumulate）、筛选（filterfalse、takewhile、dropwhile）、组合数学（product、permutations、combinations）、分组（groupby）。两个最容易踩坑的点文档都特别强调了：groupby 只会对连续相同的键分组，如果数据没有事先按分组键排序，结果会不符合预期（把相同键但不连续出现的元素分到不同组）；tee() 把一个迭代器拆成多份，但内部要为跑得慢的那一份缓存所有跳过的数据，分支之间进度差太多会导致内存占用暴涨。文末的 Recipes 部分给出了大量用这些原语组合实现常见算法的示例，值得收藏。
