---
id: nr-amz-s10-hook
node: amazon.outline
type: qa
step: 28
---
## Q
<p class="title">退款费 billing-terms 复盘<span class="meta">02 提纲</span></p>

开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
<span class="label">开场</span>

**My first blast-radius query said 196K rows; before anyone acted I found the predicate was wrong, retracted it myself, and the real number was 21,923.**

<span class="label">适用 LP</span>

- 主：**Earn Trust**、**Dive Deep**、**Are Right, A Lot**
- 副：Insist on the Highest Standards、Customer Obsession、Ownership

<span class="label">数字</span>

- 第一版：**196,274 行 / 61 商户 / ~$11,123**（谓词：credit 计划 monthly ∧ 费用创建当天生效计划 daily/net ∧ 生成的 billing_terms 仍 MONTHLY）
- 修正（加 `ps_curr.created_at <= bf.created_at`）：**21,923 行 / 10,330 credits / 30 商户 / $5,854.52**
- 1,062 个切到 NET 的美国商户里只有 **5 个**产生 bug 费用
- 那家电商：**216 行**、延迟 **214 天**
- 上游"计划写入滞后" **1 小时 32 分**
- $ 口径：`SUM(ABS(amount))/100`
- 回填：TEMU/SHEIN **191,191** 笔 sales → **382,382** fee 行

<div class="sources"><b>表达 · business English</b><br>• <b><i>an order of magnitude off</i></b> — 差了一个数量级<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“My first number was nearly an order of magnitude off: 196K rows versus about 22K.”</span><br>• <b><i>sanity-check</i></b> — 复核常理<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I sanity-checked the predicate before sharing the result widely.”</span><br>• <b><i>tighten the scope</i></b> — 收窄范围<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Adding one condition tightened the scope from sixty merchants to thirty.”</span></div>
