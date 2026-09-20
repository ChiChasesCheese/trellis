---
id: problems-payment-system-append-only-reversing-entries
node: problems.commerce.payment-system
type: qa
step: 5
tags: [grown]
---
## Q
In a payment system's double-entry ledger, why are ledger entries never updated or deleted, and how is a mistaken charge corrected instead?

## A
Ledger entries are append-only and immutable so the ledger always carries a full audit trail: if a mutable balance column were updated in place, a bug that only applies half of a transaction (crashing between two `UPDATE`s) silently leaves the ledger unbalanced with no history to diagnose it from. A mistaken or reversed charge is instead corrected with a new **reversing entry** that moves the same amount in the opposite direction — both the original and the correction stay in the log permanently, so the ledger's history is never rewritten, only extended.

## Q zh
在支付系统的双录账本中，为什么账本分录从不被更新或删除？一笔记错的收款是如何被更正的？

## A zh
账本分录追加写、不可变，这样账本始终携带完整的审计轨迹：如果用可变余额列原地更新，一个只更新了半笔交易的 bug（崩溃在两次 `UPDATE` 之间）会无声地让总账失衡，且没有历史可用来诊断。一笔记错或需要撤销的收款,不是被修改,而是用一笔金额相同、方向相反的**冲正分录（reversing entry）**去抵消——原始记录和冲正记录都永久保留在日志里,账本的历史从不被改写,只会被追加。
