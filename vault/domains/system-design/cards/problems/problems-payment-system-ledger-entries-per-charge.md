---
id: problems-payment-system-ledger-entries-per-charge
node: problems.commerce.payment-system
type: qa
step: 1
tags: [grown]
---
## Q
In a payment system design, one charge touches four ledger accounts (customer clearing, merchant payable, platform fee revenue, PSP fee expense). Why does this 4x entry-per-charge multiplier, not the raw charge QPS, drive the storage design?

## A
Every charge posts 4 immutable `LedgerEntry` rows instead of 1. At an assumed 1.2 billion charges/year (≈3.29M/day), that is ≈13.15M entries/day, ≈1.2 TB/year at 250 bytes/entry, ≈3.6 TB/year at 3x replication — small in absolute bytes, but every byte must be strongly durable and multi-replicated (never cache-rebuildable), which rules out any storage class that tolerates loss. The design lever isn't total throughput, it's that the entry count is a fixed multiple of the charge count and none of it is disposable.

## Q zh
在支付系统设计中，一次收款会触及四个账本账户（客户待清算、商户应付、平台手续费收入、PSP 手续费支出）。为什么是这个每笔收款 4 倍的分录展开倍数，而不是原始的收款 QPS，驱动了存储设计？

## A zh
每笔收款会写入 4 条不可变的 `LedgerEntry`，而不是 1 条。按假设的年 12 亿笔收款（约 329 万笔/天）估算，约为每天 1315 万条分录，每条 250 字节约 1.2 TB/年，三副本约 3.6 TB/年——绝对字节数不大，但每个字节都要求强持久化、多副本（绝不允许靠缓存重建）,这直接排除了任何“允许丢失”的存储选型。设计杠杆不是总吞吐，而是分录数是收款数的固定倍数，且没有一个字节是可丢弃的。
