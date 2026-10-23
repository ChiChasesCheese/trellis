---
id: hl-sd03-oms
node: system-design.sd03-low-latency-trading
type: qa
step: 18
---
## Q
订单管理（OMS）的状态机和关键细节是什么？ClOrdID 为什么要全局唯一且单调？

## A
每张订单一个状态机：`PENDING → WORKING → PARTIALLY_FILLED → FILLED / CANCELED / REJECTED`。关键细节：
- **PENDING 也算「已在市场里」**：发出去、回报没回来，风险上必须按可能已成交处理，最坏情况仓位包含它；
- 回报可能**重复**（at-least-once）：以 `execId` 去重，终态订单收到旧回报只是重复，不是错误；
- 回报可能**乱序或缺失**（会话重连后补发）：以交易所的会话序号 / 执行序号判断，对不上则进入「未知状态」；
- 成交价必须满足限价约束，超量成交为非法转移：**非法转移不改状态，报警**；
- 仓位 = 成交回报的函数（FIFO 配对、整数）。

客户端订单 id（ClOrdID）必须**全局唯一且单调**（含会话 id + 序号），重启后继续递增；否则交易所会把重启后的新单当作重复而拒绝，或更糟地把旧单当作新单。
