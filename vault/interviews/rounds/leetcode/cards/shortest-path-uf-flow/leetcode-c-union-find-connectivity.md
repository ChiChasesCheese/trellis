---
id: leetcode-c-union-find-connectivity
node: shortest-path-uf-flow.union-find-connectivity
type: cloze
anki: 1787102263707
tags: [concept-cloze, leetcode, recall]
---
在按秩合并（union by rank）的并查集实现中，union 时应把秩较小的树根挂到秩较大的树根下；当两棵树的秩{{c1::相等}}时，合并后新根的秩需要{{c2::加1}}，否则树高度会失控增长。

如果不按秩合并（例如总是把 x 挂到 y 下），最坏情况下树会退化成链，find 操作退化为 O(n)。按秩合并配合路径压缩后，树高度接近 O(log n)，均摊复杂度接近 O(α(n))。

**Evidence**

rank启发式保证树高度较小（接近log n）；rank比较时用<=而非<，配合rank相同时+1，保证平衡

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E5%B9%B6%E6%9F%A5%E9%9B%86%E8%BF%9E%E9%80%9A%E6%80%A7)
