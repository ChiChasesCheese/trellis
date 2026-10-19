---
id: nr-amz-s4-hook
node: amazon.s4
type: qa
step: 1
---
## Q
【S4 · AU Amex 退款费（用一条查询结束 50 条回复）】开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
**A product manager's escalation bounced through three teams for 50 replies; I ended it the same day with one query anyone could re-run.**

**适用 LP**

- 主：**Customer Obsession**、**Dive Deep**、**Earn Trust**
- 副：Are Right A Lot、Have Backbone、Ownership

**数字**

- **50 条回复 / 3 个团队**，线程路由到我之前
- 六个月退款费行数：美国 **~1,079,627**、英国 **294**、澳洲 **0**
- **157** 个 AU 商户；**288 万**笔 AU non-agg Amex 销售
- 所有 AU 商户 `fee_refund_policy` = **partial**（或 none）；退款费逻辑只在 **full** 触发
- 定性："predates the migration"
- 结果：**当天**结束线程，转成功能票 "REFUND_FEE calculation pipeline in Snowglobe"
