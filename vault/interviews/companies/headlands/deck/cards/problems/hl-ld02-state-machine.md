---
id: hl-ld02-state-machine
node: problems.ld02-trading-ood
type: qa
step: 3
---
## Q
订单状态机的合法转移表是什么？非法转移怎么处理，`PENDING` 为什么要特别说明？

## A
有限状态机（FSM）= 一组状态 + 一组事件 + 一张「在状态 S 收到事件 E 变成 S'」的表；表里没有的格子**非法**。不显式写表，状态散落在一堆 `if` 里：订单已 `FILLED` 又收到 `Fill`（重复投递或 bug）会悄悄把已成交数量加第二遍、仓位翻倍；已 `CANCELED` 却又被成交变幽灵订单。

| 当前状态 | Ack | Fill | Cancel | Reject |
|---|---|---|---|---|
| PENDING | → WORKING | 非法 | 非法 | → REJECTED |
| WORKING | 非法 | → PARTIALLY_FILLED 或 FILLED | → CANCELED | 非法 |
| PARTIALLY_FILLED | 非法 | → PARTIALLY_FILLED 或 FILLED | → CANCELED（已成交部分保留） | 非法 |
| FILLED / CANCELED / REJECTED | 非法 | 非法（重复 Fill 例外） | 非法 | 非法 |

「非法」= 抛 `IllegalTransitionException`，**订单状态不变**。终态 `FILLED/CANCELED/REJECTED` 不再变。

- `Cancel` 是**撤单确认**（不是撤单请求）；`PENDING` 状态下收到 `Cancel` 非法（真实系统里是竞态，这里简化）；
- `Reject` 带原因字符串，存进 `rejectReason`；
- **`PENDING` 订单计入未完成**：它已经发出去，可能随时成交，回报滞后但风险不会；否则「连续快速下多张单，每张都通过，合起来超限」；
- `OrderView(order, status, cumQty, cumNotional, rejectReason)`，`leavesQty()`：已撤销 / 已拒绝为 0，FILLED 为 0；
- `submit`：登记为 PENDING；重复 id → `IllegalArgumentException`；null → NPE；`get` 未知 → `NoSuchElementException`；`open()`、`all()` 按 id 升序。

Java 实现：状态用 `enum`（不是字符串）；事件用 `sealed interface ExecEvent permits Ack, Fill, Cancel, Reject` + record（`Fill(orderId, execId, qty, px)` 紧凑构造器校验 qty、px > 0；`Reject(orderId, reason)` 要求 reason 非 null）；转移用 `switch` 表达式穷尽匹配，加 `default` 反会掩盖「新增事件类型忘了处理」。

边界：表里每个非法格；终态后任何事件；重复 Ack；`PENDING` 收到 `Fill/Cancel`；`Reject` 出现在 `WORKING`。
