---
id: hl-omap-misconceptions
node: foundations.ordered-maps-trees
type: qa
step: 33
---
## Q
有序 Map 方面常见的七个误区是什么？

## A
1. 「`TreeMap` O(log n) 所以只比 `HashMap` 慢一点点」：`get` 215 ns 对 10 ns，约 20 倍，原因是指针追逐；
2. `headMap(k)` 包含 k：不包含（`headMap(k, true)` 才含），`tailMap(k)` 包含 k；
3. 用 `firstKey()` 判断空：空 Map 抛 `NoSuchElementException`，`firstEntry()` 返回 `null`；
4. `floorKey` 返回 `null` 时直接解包：`int p = map.floorKey(x);` 在 `null` 时 NPE；
5. 订单簿里一价位一个订单：同价订单因比较器相等互相覆盖，key 带序号或 value 是队列；
6. `headMap(k).size()` 当 rank 用：O(n)；
7. 遍历中修改：`for (var e : map.entrySet()) map.remove(...)` 抛 `ConcurrentModificationException`。
