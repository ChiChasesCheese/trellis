---
id: hl-hc05-treemap
node: problems.hc05-market-order-book
type: qa
step: 5
---
## Q
订单簿为什么用 `TreeMap` 存价位？买盘怎么让两边都能用 `firstEntry()` 取最优价？

## A
需要「最优价」，成交吃光一档后要立刻知道下一档。`HashMap<价格, 价位>` 不能答最小价格（要扫全部 key，O(L)）；排好序的 `ArrayList` 取最小 O(1) 但**插入新价位**要挪元素 O(L)；`TreeMap` 取最小、插入、删除都是 **O(log L)**（L = 价位数，远小于订单数）。

`TreeMap` 是红黑树：自平衡二叉搜索树（根黑；红节点的孩子黑；任一节点到所有叶子路径上的黑节点数相同），最长路径不超过最短路径两倍，高度 ≤ 2·log₂(n+1)。普通 BST 按顺序插入 1,2,3,4,5 会退化成「棍子」，查找 O(n)。

```java
TreeMap<Long, String> asks = new TreeMap<>();
asks.firstEntry();       // 最小 key，O(log n)
asks.pollFirstEntry();   // 取出并删除最小项
TreeMap<Long, String> bids = new TreeMap<>(Comparator.reverseOrder());
bids.firstEntry();       // 比较器下「最小」= 数值最大 = 最高买价
```
买盘最优价是**最高**价，所以买盘用 `Comparator.reverseOrder()`，两边都用 `firstEntry()` 取最优价，代码对称。key 类型 `Long` 是对象，会自动装箱。

声明成 `SequencedMap<Long, PriceLevel>`（Java 21）表明只用到有序、取头尾的能力。C++ 里用 `std::map`：`begin()` O(1)，`rbegin()` O(log L)；买盘最优是最后一个。
