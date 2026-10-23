---
id: hl-hc05-execute-events
node: problems.hc05-market-order-book
type: qa
step: 9
---
## Q
`execute(Command)` 对每种命令产生什么事件？拒绝（`Rejected`）的原因和检查顺序是什么？溢出为什么要在撮合之前检查？

## A
| 命令 | 事件 |
|---|---|
| `Limit(id, side, price, qty)` | 若干 `Trade(takerId, makerId, takerSide, price, qty)`，剩余非 0 再来一个 `Rested(id, side, price, remaining)` |
| `Market(id, side, qty)` | 若干 `Trade`；有剩余则 `Cancelled(id, remaining)` |
| `Cancel(id)` | `Cancelled(id, remaining)` |
| `Modify(id, newQty)` | `Modified(id, oldQty, newQty)`，**不触发撮合** |

任何失败返回**单个** `Rejected(id, reason)` 且**不改变簿**，检查顺序 `id → price → quantity → 簿状态`：`invalid id`、`invalid price`、`invalid quantity`、`duplicate id`（新单 id 已在簿上）、`unknown id`（撤 / 改不在簿上的 id，包括已成交完的）、`overflow`。

**`overflow`**：限价单挂簿后会让**自己那一侧同价位**总量溢出 → 整单拒绝，**且不先去吃对手盘**。原因：限价单最后可能挂簿，撮合完才发现挂不进去，成交事件已发出收不回，会得到「成交了一半却报溢出」的非原子结果；先保守检查，宁可误拒也不做半件事。`Modify` 增量溢出同理。

校验用 sealed switch + `when` 守卫：`case Limit l when l.price() <= 0 -> INVALID_PRICE`——**从上到下第一个匹配的生效**，更具体的错误写前面；不加守卫的兜底分支写后面，否则编译器报「被支配」（dominated）。

文本接口：`LIMIT id BUY|SELL price qty`、`MARKET id BUY|SELL qty`、`CANCEL id`、`MODIFY id newQty`；大小写不敏感；`replay` 跳过空行和 `#` 行，格式错抛 `IAE`，信息以 `line N`（N 从 1 起）开头。
