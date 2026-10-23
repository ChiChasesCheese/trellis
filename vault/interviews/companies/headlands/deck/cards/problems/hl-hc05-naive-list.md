---
id: hl-hc05-naive-list
node: problems.hc05-market-order-book
type: qa
step: 4
---
## Q
订单簿最笨的解法（所有订单放进一个 `ArrayList`）是什么？它为什么慢，需要哪几步改进？

## A
最笨：`List<Order> all`，`cancel` 用 `removeIf` 扫一遍，`bestBid` 扫一遍取 BUY 的最大价，撮合每轮扫一遍找对面最优且同价里最早的。**正确而且短，但每个操作 O(n)**：10 万张单、10 万条命令要 10¹⁰ 次比较，几十秒；一张大单扫穿 100 个价位要扫 100 遍整表。

对比：100 万订单每秒 100 万次撤单，O(n) 要 10¹² 次操作（约 1000 秒）；O(log n) 约 2×10⁷；O(1) 毫秒级。

**改进路线**：
1. 买卖盘分开（`bids` / `asks`）；
2. 按价位分组，价位放进有序 Map `TreeMap<价格, 价位>`，最优价 `firstEntry()` O(log L)；买盘用 `Comparator.reverseOrder()`；
3. 价位内 FIFO 队列保证时间优先；
4. 撤单太慢 → `byId` 哈希表 + 价位内用 `LinkedHashMap` 按 id O(1) 摘除；
5. 价位缓存 `total`；
6. 改量的优先级规则；
7. 撮合循环；
8. sealed 事件类型；
9. 热路径零分配（Part 4）。
