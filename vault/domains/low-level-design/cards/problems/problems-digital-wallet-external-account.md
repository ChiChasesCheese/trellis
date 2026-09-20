---
id: problems-digital-wallet-external-account
node: problems.marketplaces.digital-wallet
type: qa
step: 2
tags: [grown]
---
## Q
在数字钱包设计里，充值和提现只涉及一个用户账户，怎么让它们也满足“每一次资金移动都是两条分录”这条双分录（double-entry）承诺？

## A
引入一个保留的系统账户 `EXTERNAL`，代表“系统外部”。充值是 `EXTERNAL → 用户账户` 的一次移动，提现是 `用户账户 → EXTERNAL`，转账是两个真实账户之间——三者全部收敛到同一个私有原语（比如 `_move`），因此自动获得同一套加锁、记账、幂等检查逻辑，不需要为充值和提现单独写一遍。唯一的特殊之处：`EXTERNAL` 允许余额为负（代表钱从系统外部持续注入），且必须在面向用户的转账接口里显式拒绝把 `EXTERNAL` 当成转账的任意一端，否则任何调用方都能绕过余额校验凭空转账。
