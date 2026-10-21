---
id: nr-amz-s3-hook
node: amazon.outline
type: qa
step: 7
---
## Q
<p class="title">ACH 费用 NULL 事故<span class="meta">02 提纲</span></p>

开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
<span class="label">开场</span>

**A health check I built paged us because fees were silently missing — I found the cause in minutes, then removed the whole class of bug.**

<span class="label">适用 LP</span>

- 主：**Dive Deep**、**Ownership**、**Insist on the Highest Standards**、**Have Backbone**
- 副：Customer Obsession、Bias for Action、Earn Trust、Deliver Results

<span class="label">数字</span>

- 受影响 **~196 商户**，**~$11.3M/天** GMV：说 "roughly two hundred merchants, on the order of ten million dollars a day"
- 缺失 **~99,700** 笔 settled 费 + **~5,500** 笔 discount 费；累计 ~1.79M pending 行
- 切片：**100%** us_bank_account，**100%** STANDARD_ACH
- 事故发生在 standard-ACH **灰度**阶段（M2）；告警每日 **13:30 CT**
- 根因定位只说 "a few minutes"
- e2e 没抓到的 **4 个原因**

<div class="sources"><b>表达 · business English</b><br>• <b><i>on the order of ten million dollars a day</i></b> — 每天约一千万美元的量级<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“About two hundred merchants, on the order of ten million dollars a day, were affected.”</span><br>• <b><i>a hundred percent of</i></b> — 百分之百都是<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A hundred percent of the missing fees were standard-ACH bank-account transactions.”</span><br>• <b><i>rule out</i></b> — 排除（某个可能原因）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I ruled out timing lag because every age bucket had zero percent coverage.”</span></div>
