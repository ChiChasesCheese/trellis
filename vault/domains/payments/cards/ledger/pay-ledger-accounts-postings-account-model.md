---
id: pay-ledger-accounts-postings-account-model
node: ledger.accounts-postings
type: qa
step: 2
---
## Q
账本里的"账户"具体长什么样？账户的类型、币种和归属怎么设计，命名有什么讲究？

## A
**账户**是余额的承载单元，每个账户固定一个币种、一个类型，创建后不可改。

**核心字段**
- `account_id`：稳定且不复用。
- `type`：资产、负债、收入、费用、权益，决定余额的正常方向。
- `currency`：ISO 4217 币种代码。一个账户只记一种币种。
- `owner`：归属方，如某用户、某商户、平台自己、某渠道。
- `purpose`（科目）：这个账户的用途。
- 可选：`allow_negative`（是否允许透支）。

**命名约定的例子**（示意）
- `user:123:wallet:USD`：用户 123 的美元钱包余额（负债）。
- `merchant:88:payable:USD`：欠商户 88 的待结算款（负债）。
- `platform:fee_revenue:USD`：平台手续费收入。
- `channel:psp_a:receivable:USD`：PSP A 应收的在途资金（资产）。
- `platform:bank:citi:USD`：银行存款（资产）。

**设计原则**
1. 科目（purpose）固定且数量少，归属（owner）是动态的：新增一个商户就是新增一批账户，不改模型。
2. 同一属主在同一科目、同一币种只有一个账户（或有明确的子账户规则）。
3. 账户的类型和币种在创建时写死，永不修改；需要变化就新建账户并转移余额。
