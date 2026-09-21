---
id: groupby-requires-presorted-input
node: iteration.itertools
type: qa
source: python-docs
---
## Q
为什么用 `itertools.groupby()` 之前几乎总要先对数据按同一个 key 函数排序？不排序会出什么错？

## A
`groupby()` 只在相邻元素的 key 值发生变化时才切出新分组，不会像 SQL 的 GROUP BY 那样跨越整个序列聚合相同 key 的元素。如果数据没有按这个 key 预先排序，相同 key 的元素一旦被不相邻的其他元素隔开，就会被拆成多个不连续的组——这是一个悄无声息的逻辑错误，不会抛异常提醒你。
