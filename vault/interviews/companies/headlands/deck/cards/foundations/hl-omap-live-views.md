---
id: hl-omap-live-views
node: foundations.ordered-maps-trees
type: qa
step: 24
---
## Q
`TreeMap` 的 `headMap` 子视图是拷贝还是活视图？往视图里写超出范围的 key 会怎样？子视图的 `size()` 有什么性能坑？

## A
是**活视图**，看的是同一棵树。例：`cheap = asks.headMap(104, true)` 之后 `asks.put(102, 5)`，`cheap` 变成 `{101=50, 102=5, 103=20}`。往视图里 `put(200, 1)`（超出范围）抛 `IllegalArgumentException`。

性能坑：子视图的 `size()` 是 **O(元素个数)**（要遍历计数），100 万 key 的 `TreeMap` 上 `headMap(900_000).size()` 约 3 ms / 次。想要「≤ k 的有多少个」（rank）用 Fenwick 树或 order-statistic tree，不要 `headMap(k).size()`。
