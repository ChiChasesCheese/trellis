---
id: cc-transfer-oa-payments-vocabulary
node: transfer.stripe-oa
type: qa
---
## Q
The statement says "a dispute reverses the charge" and "amounts are in minor units". Why does knowing that vocabulary *before* the round matter, and what is the shortlist?

## A
**Domain words are compression: each one saves a paragraph of re-reading and prevents a modelling mistake.**

- charge / refund / **dispute** (a chargeback — reverses a charge, and can later be won back) / payout / settlement / reconciliation
- **minor units** (cents; zero-decimal currencies such as JPY have none) / **idempotency key** (a repeat must be a no-op, never a second effect) / **MCC** (merchant category code) / **BIN** (issuer prefix of a card number)
- subscription / proration / graduated vs volume tiers / included allowance / percent-plus-fixed fee

Reading the glossary of whatever domain the company works in costs twenty minutes once, and is the highest-yield preparation available: it converts an unfamiliar specification into a familiar one before the clock starts.

## Q zh
题面写着「dispute 会冲正这笔 charge」和「金额以最小单位计」。为什么*在开考前*就懂这些词很重要？清单是什么？

## A zh
**领域词汇就是压缩：每个词省下一段重读，并防住一个建模错误。**

- charge / refund / **dispute**（拒付 —— 冲正一笔 charge，之后还可能被商户申诉赢回）/ payout / settlement / reconciliation
- **最小单位**（分；JPY 这类零小数币种没有小数）/ **幂等键**（重复必须是空操作，绝不能产生第二次效果）/ **MCC**（商户类别码）/ **BIN**（卡号的发卡行前缀）
- subscription / proration（按比例摊算）/ 阶梯计价的 graduated 与 volume / 包含额度 / 百分比加固定费

把目标公司所在领域的术语表读一遍，一次花二十分钟，是收益最高的准备：它在计时开始之前就把一份陌生的规格变成熟悉的规格。
