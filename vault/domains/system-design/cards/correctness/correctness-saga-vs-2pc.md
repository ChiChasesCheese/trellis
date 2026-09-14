---
id: correctness-saga-vs-2pc
node: correctness.saga
type: qa
---
## Q
Why do payment/order systems use sagas instead of distributed transactions (2PC) across services — and what do you give up?

## A
2PC requires every participant to hold **locks while blocked on a coordinator** — across heterogeneous services (some of which are external APIs that simply don't speak 2PC), that means unbounded lock holding and availability coupled to the slowest participant.

A **saga** replaces the atomic transaction with a sequence of local transactions, each with a **compensating action** to semantically undo it on failure.

You give up **isolation** (the "I" in ACID): intermediate states are visible to other transactions — an order can be seen "reserved" and then get cancelled. Atomicity becomes "eventually all steps or all compensations."

## Q zh
为什么支付/订单系统用 saga 而不是跨服务分布式交易（2PC）— 你放弃什么？

## A zh
2PC 要求每个参与者在**协调器阻塞时持有锁** — 跨异构服务（其中一些是根本不说 2PC 的外部 API），意味着无界锁持有和可用性耦合到最慢参与者。

**saga** 将原子交易替换为本地交易序列，各自有**补偿动作**在失败时语义撤销。

你放弃**隔离**（ACID 的「I」）：中间状态对其他交易可见 — 订单可被看到「已预留」然后被取消。原子性变成「最终所有步骤或全部补偿」。
