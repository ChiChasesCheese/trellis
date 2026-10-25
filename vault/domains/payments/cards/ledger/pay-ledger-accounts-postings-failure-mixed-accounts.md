---
id: pay-ledger-accounts-postings-failure-mixed-accounts
node: ledger.accounts-postings
type: qa
step: 7
---
## Q
把"待结算"和"可提现"混在同一个商户账户里，会引发什么事故？账户设计怎么避免？

## A
**事故过程**
1. 商户账户只有一个 `merchant:88:balance`，每笔支付成功就给它加钱，不区分渠道是否已结算。
2. 提现接口只检查这个余额是否足够。
3. 商户当天有 5 万美元新订单，余额显示 5 万，立刻申请提现 5 万，通过。
4. 两天后其中 2 万美元的订单被拒付，渠道从后续结算里扣回，平台已经把钱付出，账面出现 2 万美元缺口，商户余额变负且难追回。

**根因**：账户语义不清，一个账户同时承载了"我们欠你，但渠道还没付给我们"和"我们欠你，且钱已经到手"两种性质。

**账户设计**
- `merchant:88:pending:USD`：已请款、渠道未结算，不可提现。
- `merchant:88:available:USD`：渠道已结算、过了账期，可提现。
- `merchant:88:reserve:USD`：保证金，到期释放。
- 结算确认是一条 journal：借 pending，贷 available。提现只能动 available。

**补充规则**
1. 每个账户的状态含义写进科目定义。
2. 提现检查的是 available，并用条件更新防并发超提。
3. 不允许负余额的账户，在数据库层约束；允许负的（如商户 pending 因退款变负）要有后续抵扣规则。
