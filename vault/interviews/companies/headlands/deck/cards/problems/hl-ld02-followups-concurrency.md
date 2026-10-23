---
id: hl-ld02-followups-concurrency
node: problems.ld02-trading-ood
type: qa
step: 13
---
## Q
追问：多个线程同时提交订单怎么办？市价单怎么支持？每秒 100 万个事件够吗？

## A
- **多线程**：用**单写者**——一个线程独占 `TradingDesk`，其他线程把命令投递到它的 MPSC 队列。加锁的问题：锁竞争和上下文切换进入延迟；线程交错顺序每次不同，破坏重放，除非把实际处理顺序记进日志。并行靠**按标的分片**（每片一个 desk），而不是一个 desk 里加锁。
- **市价单**：没有 `px`，价格带无法检查：用参考价（或对手方最优价）加保护价（marketable limit）近似；名义金额用保护价估算；`Fill` 的限价约束改为保护价。很多交易所不支持裸市价单，系统常把市价单转成带保护价的限价单，风控规则不用特判。
- **每秒 100 万个事件够吗**：约 2200 万事件/s（平均，JIT 预热后）吞吐够；µs 级尾延迟不够，因为每事件分配 record、`HashMap<Long,…>` 装箱、`ArrayList` 增长都产生垃圾造成 GC 停顿。改进：原语哈希表、订单槽位预分配 + 空闲链表、journal 用预分配环 / mmap、事件用 flyweight 视图。先测量再优化。
- **撤单请求与确认**：加 `PENDING_CANCEL` 状态：`WORKING/PARTIALLY_FILLED --请求--> PENDING_CANCEL`，期间仍可成交（`--Fill--> 仍可成交`），`--确认--> CANCELED`，`--撤单拒绝--> 回到原状态`（需记住）；`OrderStatus.isOpen()` 仍 true；新增事件 `CancelRequest(orderId)`，编译器会逼你在 `apply` 的 switch 里处理；风控最坏情况仓位期间仍计入剩余数量。
- **订单改单（replace）**：新数量 / 新价格，保持 / 丢失时间优先级。
- **多币种 / 合约乘数 / 手续费**：PnL 加一个 `multiplier`，费用作为单独事件。
- **风控做成责任链** `List<RiskCheck>`，讨论顺序依赖与短路。
- **record 的 `equals` 比较两个 desk**：逐字段比较，嵌套 record 递归，`OrderView` 里是 `long/String/枚举`所以安全；字段若是可变集合则比较当时内容。
- **为什么 PENDING 订单也算未完成**：回报是滞后的，风险不是。
- **订单簿 + 撮合**（把交易所一侧也建模）是另一道题：订单簿题。
