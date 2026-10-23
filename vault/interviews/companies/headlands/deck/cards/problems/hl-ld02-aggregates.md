---
id: hl-ld02-aggregates
node: problems.ld02-trading-ood
type: qa
step: 5
---
## Q
`OrderManager` 的聚合量 `openCount` 和 `openLeaves(symbol, side)` 为什么要增量维护？怎么保证不漂移？

## A
风控对每个订单都要问「这个标的这个方向未完成订单的剩余数量之和」和「一共几张未完成订单」。扫描所有订单是 O(n)，总 O(n²)。把这两个量作为状态，每次状态变化同步更新，查询 **O(1)**：
- `submit`：+qty（`openCount++`）；
- `Fill`：−成交量（`reduceOpen(s, f.qty())`）；
- `Cancel` / `Reject`：−剩余量（`reduceOpen(s, s.leaves())`）；
- 到达终态（FILLED / CANCELED / REJECTED）时 `openCount--`。

`PENDING` 订单计入未完成。多标的互不影响（按「标的 × 方向」分别统计）。

**代价**：所有会改变订单的地方都要记得更新，漏一处就漂移，而且这类 bug 只有用**随机事件流 + 逐单重算**对照才能抓到（聚合量在某个终态路径上漏了更新）。边界：`Cancel/Reject/全部成交` 后释放；随机事件流下与逐单重算一致。

相关复杂度：每个事件 O(1)；`PositionBook.onFill` 摊还 O(1)（每个 lot 只入队一次、出队一次）；`get/netQty` 要遍历该标的的 lot 队列 O(lot 数)；风控 `check` O(1) 加上 `netQty` 的那次 lot 遍历；`open()/all()` 要排序 O(n log n)，只用于查询（输出前排序保证确定性，不依赖 `HashMap` 遍历顺序）。

基准（JIT 预热后取 5 次中位数）：实时处理 40 万事件 17.7 ms（22.6 M 事件/s，44 ns/事件）；重放 40 万事件 17.1 ms（23.4 M/s）；`PositionBook.onFill` 300 万次成交 103 ms（29 M 次/s，含 `"S"+i` 字符串分配）。这是平均吞吐量级，不含 GC 尾延迟；实现用 `HashMap<Long,…>`、装箱、record 分配，没做零分配优化。µs 级尾延迟需要：原语哈希表、预分配订单槽位 + 空闲链表、journal 用预分配环 / mmap、flyweight 事件视图；先测量再优化。
