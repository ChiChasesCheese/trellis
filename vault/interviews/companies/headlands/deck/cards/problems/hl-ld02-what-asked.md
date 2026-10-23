---
id: hl-ld02-what-asked
node: problems.ld02-trading-ood
type: qa
step: 1
---
## Q
交易 OOD 题（订单状态机、仓位 PnL、交易前风控、事件溯源）的四个 Part 和共同约定是什么？

## A
- **Part 1 `OrderManager`**：订单状态机 `PENDING → WORKING → PARTIALLY_FILLED → FILLED`，另有 `CANCELED`、`REJECTED`；回报去重；聚合量增量维护；
- **Part 2 `PositionBook`**：按标的维护仓位，FIFO 配对，已实现 / 未实现盈亏，**翻转**；
- **Part 3 `RiskEngine`**（`RiskLimits`、`RiskResult`、`RiskReason`）：交易前风控——数量 / 名义金额 / 价格带 / 未完成订单数 / **最坏情况仓位**，熔断开关；
- **Part 4 `TradingDesk`**：把 1–3 装配起来，输入先进 journal 再处理，`replay` 重放。

**共同约定**：
- 价格是整数 tick，数量是整数股数（`long`），没有浮点，PnL 逐位可验证；名义金额 = `px * qty`，用 `Math.multiplyExact`，溢出是异常而不是回绕；
- `Order(id, symbol, side, qty, px)` 是限价单（没有市价单），紧凑构造器保证 `id > 0`、`qty > 0`、`px > 0`、`symbol` 非空白；
- 输出确定：所有列表按 id 升序 / 符号字典序；
- **先验证、后修改**：任何抛异常的路径都不能改变状态（Part 4 重放依赖这点）；
- 单线程使用，不加锁。

评分点是建模质量而非算法：(1) 用类型表达不变量（record 紧凑构造器、sealed 事件 + 穷尽 switch、enum 状态）；(2) 状态机显式化，非法转移抛异常且不改状态；(3) 整数与溢出意识；(4) **fail closed**，拿不准就拒绝；(5) 可扩展，新增风控规则 / 事件要改哪里；(6) 决定性与可重放。

大白话：下单后陆续收到回报 Ack（收到了）、Fill（成交），程序要回答订单现在什么状态、还能成交多少，持有多少股赚了多少，新订单能不能发，以及崩了怎么恢复到一模一样的状态。
