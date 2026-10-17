%% trellis:begin %%
# 数字钱包（Digital Wallet）
*设计题（Design Problems） / 交易与撮合*

充值、转账、交易记录，余额不能为负且转账两边一致。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/low-level-design/map/concurrency.hazards|死锁及其亲戚]]

**Unlocks:** [[domains/low-level-design/map/amazon.amz-wallet|钱包与账户（Wallet / Bank Account）（low priority）]]

## Readings
- [[solution-digital-wallet|设计题解：数字钱包（Digital Wallet）]]
- [[src-algomaster-digital-wallet|AlgoMaster — Low Level Design (LLD)]]
- [[src-github-digital-wallet|Design a Digital Wallet Service | LLD | Low Level Design]]

## Drills
- [[design-digital-wallet|Drill：数字钱包（Digital Wallet）]]

## Cards (8)
1. [[problems-digital-wallet-transfer-atomicity]]
2. [[problems-digital-wallet-external-account]]
3. [[problems-digital-wallet-signed-delta-not-kind]]
4. [[problems-digital-wallet-balance-cache-vs-derive]]
5. [[problems-digital-wallet-lock-ordering-stable-key]]
6. [[problems-digital-wallet-idempotency-reuses-account-lock]]
7. [[problems-digital-wallet-idempotency-conflict]]
8. [[problems-digital-wallet-ledger-append-only-idempotency-purged]]
%% trellis:end %%

## Notes
