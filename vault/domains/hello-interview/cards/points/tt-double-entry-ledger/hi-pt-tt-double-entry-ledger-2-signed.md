---
id: hi-pt-tt-double-entry-ledger-2-signed
node: tt.lld.tt-double-entry-ledger.points
type: qa
step: 1
---
## Q
**复式账本（类设计） · 带符号金额的约定**｜必会 · 出自：复式账本（类设计） › 核心实体与接口

`Posting(account, currency, amount)` 里金额为什么用带符号整数？借贷方向怎么约定，用户钱包的余额怎么展示？

## A
**约定。** 整数最小货币单位，借方为正、贷方为负，所以一条分录所有腿按币种之和为 0，这是最容易检查的不变量。
**展示。** 用户钱包是负债账户（平台欠用户），余额为负，展示时取反。
**代价。** 要记住各类账户的正常余额方向。
