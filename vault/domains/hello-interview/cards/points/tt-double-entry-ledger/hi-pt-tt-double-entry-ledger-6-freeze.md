---
id: hi-pt-tt-double-entry-ledger-6-freeze
node: tt.lld.tt-double-entry-ledger.points
type: qa
step: 6
---
## Q
**复式账本（类设计） · 冻结、可用余额与不透支**｜出自：复式账本（类设计） › 深入 2

转账处理期间金额要先占住，用户钱包不能透支。怎么设计冻结，检查怎么写才不被并发击穿？

## A
**冻结。** 另设冻结表 `(账户, 冻结 ID) → 金额`，可用余额 = 账面余额展示值 − 冻结合计；冻结与释放各自幂等。
**易错。** 「写入后可用 ≥ 0」的检查必须与写入在同一把锁或事务里，否则两个并发转账各自通过、一起透支。
**SQL。** `UPDATE ... SET balance = balance - x WHERE balance >= x`，受影响行数 0 即余额不足。平台内部账户（在途资金）可以为负。
