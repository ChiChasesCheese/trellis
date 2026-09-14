---
id: distributed-saga-tradeoffs
node: distributed.transactions.distributed
type: qa
---
## Q
A saga replaces a distributed transaction with local transactions plus compensations. Precisely which ACID property do you lose, and what do you do about it?

## A
You keep **atomicity in the eventual sense** (every step either completes or is compensated) and lose **isolation**: each local step commits immediately, so other transactions can **read intermediate state** — an order that exists while payment is still pending, an inventory reservation that will be released 3 seconds from now. Classic hazards are *dirty reads* of half-done sagas and *lost updates* when another saga writes the same row mid-flight.

Countermeasures (the "semantic lock" toolkit):

- **Semantic lock**: a status flag (`PENDING`) that other workflows must respect; the saga clears it at the end.
- **Commutative updates**: model as `credit/debit` deltas rather than absolute set, so ordering stops mattering.
- **Reread value / version check** before compensating, so you don't undo someone else's newer write.

Also non-negotiable: every step and compensation must be **idempotent and retryable** (they will be re-delivered), and compensation must be *semantically* possible — you can refund a charge, but you cannot un-send an email, so put irreversible steps **last**. If the invariant truly cannot tolerate a visible intermediate state (balance must never go negative), don't use a saga — co-locate the data in one transactional store.

## Q zh
Saga 用本地事务加补偿取代了分布式事务。精确地说，你丢掉的是 ACID 里的哪一个属性？你又是怎么应对的？

## A zh
你保留的是**最终意义上的原子性**（每一步要么完成，要么被补偿），丢掉的是**隔离性**：每个本地步骤立即提交，所以其他事务可以**读到中间状态**——一个订单存在，而支付还在待定中；一份库存预留三秒后会被释放。经典的隐患是读到半途而废的 saga 造成的*脏读*，以及另一个 saga 在中途写同一行造成的*丢失更新*。

对策（"语义锁"工具箱）：

- **语义锁**：一个其他工作流必须尊重的状态标志（`PENDING`）；saga 在结束时清除它。
- **可交换的更新**：把更新建模成 `credit/debit` 这样的增量，而不是绝对赋值，这样顺序就不再重要。
- 补偿之前先**重读值/做版本检查**，这样你就不会撤销别人更新过的写入。

还有不能妥协的一点：每一步和每个补偿都必须是**幂等且可重试的**（它们会被重复投递），而且补偿必须在*语义上*是可能的——你可以退一笔款，但没法收回一封已发的邮件，所以要把不可逆的步骤放在**最后**。如果这个不变量真的容不下可见的中间状态（余额永远不能为负），就不要用 saga——把数据放进同一个事务型存储里。
