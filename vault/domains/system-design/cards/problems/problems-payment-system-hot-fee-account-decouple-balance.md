---
id: problems-payment-system-hot-fee-account-decouple-balance
node: problems.commerce.payment-system
type: qa
step: 7
tags: [grown]
---
## Q
In a payment system design processing 1.2 billion charges/year (peak ≈228 charges/sec), the platform fee account receives a credit entry on every single charge. Why does this make it a write hot spot independent of how the rest of the ledger is sharded, and what is the simplest fix?

## A
Because every charge credits the same one account, that account's write rate always equals the system's total charge rate — sharding the ledger by merchant_id doesn't help, since there's still only one fee account. If its balance were a synchronously maintained column, every charge would serialize on that one row. The fix used here: since the fee account has no overdraft invariant to check at write time, entries are appended lock-free and its balance is derived asynchronously (snapshot + replay) instead of maintained as a hot, synchronously-updated row.

## Q zh
在一个年处理 12 亿笔收款（峰值约 228 笔/秒）的支付系统设计中，平台手续费账户在每一笔收款上都会收到一笔贷方分录。为什么这会让它成为一个与账本其余部分如何分片无关的写热点？最简单的解法是什么？

## A zh
因为每一笔收款都贷记同一个账户，这个账户的写入速率永远等于系统总收款速率——按 `merchant_id` 分片账本对它毫无帮助，因为手续费账户始终只有一个。如果它的余额是同步维护的列，每一笔收款都会在这一行上串行化。这里采用的解法是：由于手续费账户没有需要在写入时强制的禁止透支不变量，分录可以无锁追加，余额异步推导（快照 + 重放），而不是维护成一个同步更新的热行。
