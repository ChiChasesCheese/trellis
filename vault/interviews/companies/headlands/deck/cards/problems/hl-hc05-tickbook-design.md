---
id: hl-hc05-tickbook-design
node: problems.hc05-market-order-book
type: qa
step: 13
---
## Q
`TickBook`（零分配订单簿）把对象图换成了哪些数组结构？每个替换为什么可行，代价是什么？

## A
| 原来 | 换成 | 为什么可以 |
|---|---|---|
| `TreeMap<Long, PriceLevel>` | 数组下标 `head[side][tick]` | 价格是有界整数 `1..maxTicks-1`，直接当下标 O(1) |
| `firstEntry()` | `bestBid` / `bestAsk` 两个 `int` + 位图 | 最优价只在价位变空 / 新价位出现时变 |
| `Node` 对象 | `long[] oid`、`long[] oqty`、`int[] oprice`、`byte[] oside` | 同一槽位号在各数组里是同一张订单（结构数组） |
| `LinkedHashMap` 队列 | `int[] prev`、`int[] next`（侵入式双向链表）+ `head/tail` | 知道槽位号就能 O(1) 摘除 |
| `new Node` | free list | 释放的槽位串起来重用 |
| `HashMap<Long, Node>` | 开放寻址 `long[] keys` + `int[] vals` | 不装箱 |
| `List<Event>` | 回调 `TradeSink.onTrade(taker, maker, price, qty)` | 调用方决定怎么处理，不建事件对象 |

`TickBook(int maxTicks, int capacity)`：价格 `long` tick，范围 `1..maxTicks-1`；订单数 ≤ `capacity`（≤ 2²²）。`limit` 返回挂簿的剩余量（0=全部成交），非法返回 `REJECTED`，池满返回 `FULL`（此时**不撮合**）；`cancel(id)` O(1)；`bestBid/bestAsk` 无则 `NONE (-1)`；`qtyAt(side, price)`。要求：200 万次随机操作 < 2 s；稳态 60 万次分配 < 512 KB；与 `OrderBook` 逐步对拍一致。

**代价**（必讲）：价格带固定，超出拒绝；订单数固定，满了返回 `FULL`——「有界内存」的取舍；代码更长、更易出 bug（手写哈希删除、链表摘除），所以用 Part 2 的 `OrderBook` 当真值对拍。

复杂度：`limit` O(成交笔数)，`cancel` O(1)，最优价变空时位图扫描最坏 O(maxTicks/64)。

价格范围很大怎么办：数组只覆盖中间价附近一段，远处价位放 `TreeMap`；或价位少时用有序数组 + 二分。
