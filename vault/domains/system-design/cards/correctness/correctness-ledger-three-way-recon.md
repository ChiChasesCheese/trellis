---
id: correctness-ledger-three-way-recon
node: correctness.ledger
type: qa
---
## Q
Payments teams reconcile three-way — internal ledger vs processor report vs bank statement. What does each pairwise match catch that two-way misses, and how are breaks classified?

## A
- **Ledger ↔ processor**: did every charge/refund we recorded happen, at the right amount/state? Catches lost webhooks, timeout-ambiguity bugs.
- **Processor ↔ bank**: did the processor's promised payouts (net of fees, chargebacks, reserves) actually **arrive as cash**? Two-way recon against the processor alone trusts their report — a processor error or insolvency shows up only at the bank.
- **Ledger ↔ bank**: closes the triangle so cash movements have ledger entries (fees, FX spreads you never booked).

Breaks are bucketed **timing** (in-flight, self-clears within a settlement window — age it, don't page) vs **true break** (investigate, then post an explicit **correcting entry**, never edit). Metrics: match rate and oldest unresolved break age ([[correctness-reconciliation]]).

## Q zh
支付团队三方对账 — 内部账本 vs 处理方报告 vs 银行对账单。两两匹配各捕什么是两方遗漏的，怎样分类断差？

## A zh
- **账本 ↔ 处理方**：每笔我们记录的扣款/退款都发生了吗，金额/状态对吗？捕 webhook 丢失、超时歧义 bug。
- **处理方 ↔ 银行**：处理方承诺的支付（净手续费、退单、预留）真的**到账为现金**？仅针对处理方的两方对账信任他们的报告 — 处理方错误或破产仅在银行显示。
- **账本 ↔ 银行**：闭合三角形，资金流动有账本分录（手续费、你未记账的 FX 点差）。

断差分为**时间类**（在途、清算窗口内自清 — 陈化，不告警）vs **真断差**（调查，然后过账显式**改正分录**，绝不编辑）。指标：匹配率和最老未解断差年龄（[[correctness-reconciliation]]）。
