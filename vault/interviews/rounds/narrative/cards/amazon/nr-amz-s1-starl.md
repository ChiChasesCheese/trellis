---
id: nr-amz-s1-starl
node: amazon.s1
type: qa
step: 2
---
## Q
【S1 · Amex 结算管线（端到端 owner）】STAR-L 提纲（60–90 秒）

## A
**S**

- **Braintree** 费用平台，跑在 **Snowflake** 上；Visa / Mastercard 走收单方近实时视图
- **Amex** 是闭环：**每天一个定宽文件**，文件确认结算前不能入账

**T**

- 我 **owner** 整条管线，从设计文档到生产；接手时只有**一张表的 stub**
- 输出喂给**费用计算和出款**

**A**

- 设计 **6 条 append-only stream**，每种记录类型一条，各有独立 **offset**，互不阻塞
- 每个阶段用**复合键 MERGE**，重发文件不会 **double-count**
- 两个**校验函数**，所有不匹配进 **error log**，不丢弃
- 一个 **feature flag** 当 **kill switch**，一条 `UPDATE`，无需发布
- 一直 **on-call**，真实故障后上了**十几个加固 PR**

**R**

- 前六个月 **~22M** 笔 Amex 交易；生产 **18 个月**
- 任期内最大 PR，**~1,800 行**

**L**

- 坏了的时候，它**记录问题而不是丢数据**
