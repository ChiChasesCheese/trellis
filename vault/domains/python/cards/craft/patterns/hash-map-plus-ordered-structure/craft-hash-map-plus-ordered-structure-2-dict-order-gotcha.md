---
id: craft-hash-map-plus-ordered-structure-2-dict-order-gotcha
node: craft.patterns.hash-map-plus-ordered-structure
type: qa
step: 2
---
## Q
**哈希表 + 有序结构 · 能不能只用普通 dict 当 LRU**｜模式

Python 3.7 起 dict 保证插入顺序。于是有人用 `d[k] = d.pop(k)` 把 key 移到末尾，用 `next(iter(d))` 取最旧的 key，不就是 LRU 了吗？为什么还需要 `OrderedDict`？

## A
**要点。** 功能上可行，但取最旧的那一步在最坏情况下不是 O(1)。CPython 的 dict 把条目存在一个数组里，删除只是留下空洞，迭代器每次从数组开头起跳过所有空洞。LRU 的访问模式正是不断从前面删，空洞会堆在前面，直到下次扩容整理。`OrderedDict` 自带链表，取头部不用扫描。

```python
d = dict.fromkeys(range(N))
for i in range(holes):
    del d[i]                  # 从前面删：数组里留下 holes 个空洞
next(iter(d))                 # 取最旧：迭代器要从头跳过所有空洞
```

N=20 万，前面分别有 0、5 万、15 万个空洞，每次 `next(iter(d))` 的耗时（实测 CPython 3.14；条目数组加空洞的设计从 3.6 起如此）：

```
前面有       0 个空洞: next(iter(d)) 每次      0.1 us
前面有   50000 个空洞: next(iter(d)) 每次     13.2 us
前面有  150000 个空洞: next(iter(d)) 每次     33.8 us
```

**为什么。** 空洞越多越慢，是线性的；绝对值很小，只在容量大、淘汰频繁时才累积成问题。

**不适合用 OrderedDict 的情况。** 需要按频率组织（LFU）时，每个频率要一条链表，就得自己写双向链表；`OrderedDict` 只能表达一条顺序。

**易错。** 把「dict 保证插入序」当成「dict 是有序容器」：它只保证遍历顺序，不提供在两端高效取放的接口。
