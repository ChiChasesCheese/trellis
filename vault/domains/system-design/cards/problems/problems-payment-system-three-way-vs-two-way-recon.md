---
id: problems-payment-system-three-way-vs-two-way-recon
node: problems.commerce.payment-system
type: qa
step: 6
tags: [grown]
---
## Q
In a payment system's reconciliation design, what does adding the bank statement as a third leg (ledger vs PSP settlement file vs bank statement) catch that a two-way ledger-vs-PSP-file reconciliation cannot?

## A
Two-way reconciliation (ledger vs PSP file) can only detect disagreements between our own records and the PSP's report — it fully trusts that the PSP's report is itself correct. The PSP-file-vs-bank-statement leg is the only comparison that checks whether the money the PSP promised to settle actually arrived as cash; if the PSP's report has an error or a payout is delayed, two-way reconciliation against the PSP alone never surfaces it, because both sides being compared originate from the same untrusted party.

## Q zh
在支付系统的对账设计中，把银行对账单加为第三方（账本 vs PSP 结算文件 vs 银行对账单）能捕获到两方对账（仅账本 vs PSP 文件）捕获不到的什么问题？

## A zh
两方对账（账本 vs PSP 文件）只能发现我们自己的记录和 PSP 报告之间的不一致——它完全信任 PSP 的报告本身是对的。PSP 文件 vs 银行对账单这一对，是唯一能核实 PSP 承诺结算的钱是否真的以现金形式到账的比对；如果 PSP 的报告本身有错，或者打款延迟了，只对着 PSP 做两方对账永远发现不了，因为被比较的两边本就来自同一个不被信任的来源。
