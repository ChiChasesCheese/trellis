---
id: correctness-ledger-multi-currency
node: correctness.ledger
type: qa
---
## Q
How does a double-entry ledger handle a customer paying EUR 100 for a USD 108 charge — what does "entries sum to zero" mean with two currencies?

## A
The zero-sum invariant holds **per currency, never across currencies** — summing EUR against USD is meaningless. An FX conversion is modeled as **two balanced legs through conversion/nostro accounts**:

- EUR leg: customer −100 EUR → EUR conversion account +100 EUR (sums to 0 in EUR)
- USD leg: USD conversion account −108 USD → merchant +108 USD (sums to 0 in USD)

The conversion accounts absorb the position; revaluing them at market rate yields **FX gain/loss**, posted as its own entries. Store the **rate and both amounts** on the transaction, as integer **minor units with per-currency exponent** (JPY has 0 decimals, BHD 3) — never floats, never a single "converted amount" that loses the original.

## Q zh
复式分录账本怎样处理客户支付 EUR 100 用于 USD 108 的费用 — "分录总和为零"在两种货币下什么意思？

## A zh
零和不变量保持**按货币，绝不跨货币** — 对 EUR 和 USD 求和无意义。FX 转换建模为**通过兑换/nostro 账户的两条平衡腿**：

- EUR 腿：客户 −100 EUR → EUR 兑换账户 +100 EUR（EUR 中总和为 0）
- USD 腿：USD 兑换账户 −108 USD → 商户 +108 USD（USD 中总和为 0）

兑换账户吸收头寸；用市场汇率重估它们产生 **FX 收益/损失**，以自己的分录过账。在交易上存储**汇率和两个金额**，作为**带按货币指数的整数最小单位**（JPY 0 位小数，BHD 3 位）— 绝不浮点，绝不单个"转换金额"损失原始。
