---
id: nr-amz-s6-hook
node: amazon.s6
type: qa
step: 1
---
## Q
【S6 · Fee anomaly detector 的 go/no-go（判断力 · 说不 · 分阶段）】开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
**I inherited a departing intern's ML detector that had only run in QA, and instead of momentum I wrote a go/no-go that split it into a safe SQL phase and a gated ML phase.**

**适用 LP**

- 主：**Are Right, A Lot**、**Dive Deep**、**Have Backbone**、**Ownership**
- 副：Frugality、Invent and Simplify、Bias for Action、Deliver Results、Insist on the Highest Standards

**数字**

- 数字来自我自己的评估文档，尚未从生产复核；口播用量级，并说明这一点
- QA **6 个合成商户** vs 生产 **18,140** 商户：说 "six synthetic merchants versus eighteen thousand"
- QA **8.3 亿行** vs 生产 **390 亿行**：说 "under a billion rows versus tens of billions"
- 峰值一天 **7.6 亿行**：说 "up to about 760 million rows on a peak day"
- **1,468** plan code；**15,293** (plan, description) 组合：说 "about fifteen thousand plan combinations"
- QA 前两个商户占 **97%** 的行
- Phase 2：**5–8 人周**编码；**2–3 个月**到生产可信
- **99.5%** 阈值 × 每天数亿行 = 每天**数百万条**告警
- 唯一不可再生的是分析师 **disposition 标注**，离职前导出
