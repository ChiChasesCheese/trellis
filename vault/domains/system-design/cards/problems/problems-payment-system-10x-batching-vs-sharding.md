---
id: problems-payment-system-10x-batching-vs-sharding
node: problems.commerce.payment-system
type: qa
step: 8
tags: [grown]
---
## Q
In a payment system at 10x its baseline volume (charges/year 1.2B → 12B, peak charge rate ≈228/sec → ≈2,283/sec), why does merchant-based ledger sharding alone fail to fix the platform fee account's hot spot, and what changes?

## A
Sharding the ledger by merchant_id spreads out merchant-specific writes, but the platform fee account is still a single account touched by every charge across every shard — its write rate scales with total system throughput, not per-shard throughput, so at 10x its peak write rate (≈2,283/sec) crosses into territory a single row genuinely can't sustain even lock-free-appended. The fix is to move from simple asynchronous derivation to short-window batching (grouping same-account operations into one atomic read-modify-write per window) rather than fragmenting the fee account's identity across sub-accounts.

## Q zh
在一个交易量达到基准 10 倍的支付系统（年收款从 12 亿到 120 亿，峰值收款速率从约 228/秒到约 2,283/秒）中，为什么单靠按商户分片账本无法解决平台手续费账户的热点问题？需要做出什么改变？

## A zh
按 `merchant_id` 给账本分片能分散商户相关的写入，但平台手续费账户仍然是一个被所有分片上的每一笔收款都触及的单一账户——它的写入速率随系统总吞吐而不是单分片吞吐扩展，因此在 10 倍规模下其峰值写入速率（约 2,283/秒）会达到一个即使无锁追加、单行也确实扛不住的量级。解法是从简单的异步推导升级为短窗口批处理（把同一账户在窗口内的操作合并成一次原子读改写），而不是把手续费账户的身份拆分到多个子账户里。
