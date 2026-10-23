---
id: hl-omap-cslm-when
node: foundations.ordered-maps-trees
type: qa
step: 30
---
## Q
什么时候用 `ConcurrentSkipListMap`，什么时候用 `TreeMap`？热点是同一个最优价时跳表能救你吗？

## A
`ConcurrentSkipListMap` 用于多个线程同时读写同一个有序 Map，且读多写少或写操作分散（如多线程更新不同价位）。单线程用 `TreeMap`，更快（put 约 230 ns 对 390 ns）。

热点就是「同一个最优价」时跳表也救不了你：所有线程竞争同一个节点。更常见的设计是**单线程拥有订单簿**。
