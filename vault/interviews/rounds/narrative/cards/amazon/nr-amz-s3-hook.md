---
id: nr-amz-s3-hook
node: amazon.s3
type: qa
step: 1
---
## Q
【S3 · ACH 费用 NULL 传播事故（最难的 bug · fail loudly）】开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
**A health check I built paged us because fees were silently missing — I found the cause in minutes, then removed the whole class of bug.**

**适用 LP**

- 主：**Dive Deep**、**Ownership**、**Insist on the Highest Standards**、**Have Backbone**
- 副：Customer Obsession、Bias for Action、Earn Trust、Deliver Results

**数字**

- 受影响 **~196 商户**，**~$11.3M/天** GMV：说 "roughly two hundred merchants, on the order of ten million dollars a day"
- 缺失 **~99,700** 笔 settled 费 + **~5,500** 笔 discount 费；累计 ~1.79M pending 行
- 切片：**100%** us_bank_account，**100%** STANDARD_ACH
- 事故发生在 standard-ACH **灰度**阶段（M2）；告警每日 **13:30 CT**
- 根因定位只说 "a few minutes"
- e2e 没抓到的 **4 个原因**
