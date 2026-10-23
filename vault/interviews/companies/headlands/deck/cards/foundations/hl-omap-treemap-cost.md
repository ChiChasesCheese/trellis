---
id: hl-omap-treemap-cost
node: foundations.ordered-maps-trees
type: qa
step: 13
---
## Q
100 万个随机 int key 上 `TreeMap` 与 `HashMap` 的 put、get 耗时各是多少？为什么 `TreeMap.get` 慢约 20 倍？

## A
- `HashMap<Integer,Integer>`：`put` 60 ns，`get` 10 ns；
- `TreeMap<Integer,Integer>`：`put` 239 ns，`get` 215 ns。

`TreeMap.get` 比 `HashMap.get` 慢约 **20 倍**，是 O(log n) 与 O(1) 加缓存行为叠加的结果：O(log n) 里每一层都是一次**指针跳转**，节点散落在堆里，层数 × 缓存未命中 = 慢。

结论：只有真的需要有序时才付这个代价。
