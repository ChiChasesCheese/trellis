---
id: cc-rules-fee-net-vs-gross
node: rules.fees
type: qa
---
## Q
A merchant is charged a fee on a payment. Does the payout line show `amount`, `amount - fee`, or `amount + fee`?

## A
**Read which side of the money the fee sits on — the spec always says, and the three answers are three different programs.**

- *Deducted* (the normal Stripe shape): the merchant receives `amount - fee`; the fee never appears as its own movement.
- *Added on top* (surcharge): the payer is charged `amount + fee`.
- *Separate row*: both the gross amount and a negative fee row appear, and the net is their sum.

Then keep signs consistent in the ledger: a fee is negative money for the merchant, so a group's net can legitimately go negative — and a negative net must still be printed, not clamped to zero.

## Q zh
商户为一笔付款支付手续费。付款行显示的是 `amount`、`amount - fee` 还是 `amount + fee`？

## A zh
**看手续费落在钱的哪一侧 —— 题面总会说，而这三种答案是三个不同的程序。**

- **从中扣除**（Stripe 的常规形态）：商户收到 `amount - fee`；手续费本身不作为一笔独立的资金变动出现。
- **额外附加**（附加费）：付款方被收取 `amount + fee`。
- **单列一行**：毛额和一行负数手续费同时出现，净额是两者之和。

然后在账本里保持符号一致：手续费对商户是负数金额，所以某组的净额完全可能为负 —— 而负净额仍要照常打印，不能被夹到零。
