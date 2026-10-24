---
id: tlc-python-itertools-functools-3-groupby
node: python.itertools-functools
type: qa
step: 3
---
## Q
**Python 工具箱｜`itertools.groupby`**

`groupby` 与 SQL 的 `GROUP BY` 有什么本质区别？游程编码（run-length encoding）怎么写？为什么分组前要排序，以及它有什么迭代器陷阱？

## A
`groupby(iterable, key=None)` 只把**连续**的、`key` 相同的元素归为一组；不连续的同键元素会分成多组。

```python
from itertools import groupby
print([(k, len(list(g))) for k, g in groupby("aaabccdd")])
# [('a', 3), ('b', 1), ('c', 2), ('d', 2)]：游程编码
print([(k, len(list(g))) for k, g in groupby("abab")])
# [('a', 1), ('b', 1), ('a', 1), ('b', 1)]：没排序，同键被拆开
words = ["eat", "tea", "tan", "ate", "nat", "bat"]
sig = lambda w: "".join(sorted(w))
print([(k, list(g)) for k, g in groupby(sorted(words, key=sig), key=sig)])
# [('abt', ['bat']), ('aet', ['eat','tea','ate']), ('ant', ['tan','nat'])]
```

- 要按值全局分组，先 `sorted(..., key=同一个 key)` 再 `groupby`，`O(n log n)`；纯分组用 `defaultdict(list)` 是 `O(n)`，更快。
- 它真正的用武之地是**连续段**：字符串压缩（LC 443）、外观数列（LC 38）、统计连续相同字符的游程。
- 每个组 `g` 是共享底层迭代器的视图，**进入下一组后上一组就失效**：

```python
g = groupby("aab"); k1, g1 = next(g); k2, g2 = next(g)
print(list(g1), list(g2))   # [] ['b']：g1 在取下一组时已被耗尽
```

要保留就在当轮 `list(g)`；`g` 是迭代器，不能直接 `len(g)`。
