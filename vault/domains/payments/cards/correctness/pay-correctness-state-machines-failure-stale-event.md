---
id: pay-correctness-state-machines-failure-stale-event
node: correctness.state-machines
type: qa
step: 7
---
## Q
一条迟到的 webhook 把已请款的订单改回了已授权，引发重复发货。事故怎么发生，怎么用状态机避免？

## A
**事故过程**
1. 订单 O1 授权成功，渠道发 webhook W1："authorized"，但推送延迟了。
2. 平台已通过同步响应得到授权结果，于是请款成功，订单状态变为 captured，仓库开始发货。
3. 渠道重试队列恢复，W1 在两分钟后到达。处理代码没有状态守卫，直接 `UPDATE order SET status = 'authorized'`。
4. 订单"回退"到 authorized。一个定时任务扫描所有 authorized 且已满足发货条件的订单，**再次触发请款和发货**。
5. 结果：请款可能被渠道拒绝或重复，仓库发出两批货，客户收到重复商品；对账出现重复请款或差异。

**根因**：状态可以倒退，且发货触发条件依赖"当前状态"而非"状态转移事件"。

**状态机的防护**
- 转移表中不存在 `captured → authorized`，写入被拒；迟到事件按阶位判断为过期，忽略并记录。
- 发货由 `authorized → captured` 这个**转移事件**（通过 outbox 发出）触发，只会触发一次；而不是靠扫描当前状态。
- 请款动作有自己的幂等键（请款单号），重复触发也不会二次请款。

**发现**
- 监控非法转移尝试的计数；这个计数不为零就说明有乱序事件，需要排查渠道。
- 对账：渠道请款笔数大于内部请款单数量。
