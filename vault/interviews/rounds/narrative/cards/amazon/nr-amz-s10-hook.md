---
id: nr-amz-s10-hook
node: amazon.s10
type: qa
step: 1
---
## Q
【退款费 billing-terms 复盘（推翻自己的数字）】开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
**My first blast-radius query said 196K rows; before anyone acted I found the predicate was wrong, retracted it myself, and the real number was 21,923.**

**适用 LP**

- 主：**Earn Trust**、**Dive Deep**、**Are Right, A Lot**
- 副：Insist on the Highest Standards、Customer Obsession、Ownership

**数字**

- 第一版：**196,274 行 / 61 商户 / ~$11,123**（谓词：credit 计划 monthly ∧ 费用创建当天生效计划 daily/net ∧ 生成的 billing_terms 仍 MONTHLY）
- 修正（加 `ps_curr.created_at <= bf.created_at`）：**21,923 行 / 10,330 credits / 30 商户 / $5,854.52**
- 1,062 个切到 NET 的美国商户里只有 **5 个**产生 bug 费用
- 那家电商：**216 行**、延迟 **214 天**
- 上游"计划写入滞后" **1 小时 32 分**
- $ 口径：`SUM(ABS(amount))/100`
- 回填：TEMU/SHEIN **191,191** 笔 sales → **382,382** fee 行
