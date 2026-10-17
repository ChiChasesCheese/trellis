---
nodes: [amazon.amz-aws-billing, patterns.strategy, oop.values]
tags: [problem]
---
# Drill：AWS 账单服务（AWS Billing Service）

一个用户在一个月里用了若干云服务，每个服务有用量和费率，要出一张每一行都能解释的月账单。
规模很小，但每一关都在检验同一件事：新需求是落在一个新类上，还是迫使你改已写好的核心方法。第 4 关选做。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：每个服务的用量乘以费率，按服务汇总成账单。想清楚钱用什么类型，什么时候舍入，总额与各行的关系。
- 第 2 关（约 15 分钟）：存储类服务要阶梯价（用量越大单价越低），函数类服务每月前一部分免费。阶梯是边际还是整体？对每条记录分档，还是对月总量分档？
- 第 3 关（约 15 分钟）：用量记录会重复上报。同一个编号再来一次、或带着不同内容再来，各怎么处理？
- 第 4 关（选做）：月中调价；不同服务用不同币种；多个线程同时上报。

**怎么练**：把 `vault/domains/low-level-design/problems/amz-aws-billing/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/amz-aws-billing -q`。

**评分点**
- 开场问了费率形状、用量来源、调价与币种（[[amz-aws-billing-how-asked-and-three-questions]]）。
- 对象职责清楚：费率、仓库、价格本、出账单各有变化原因（[[amz-aws-billing-objects-and-their-jobs]]）。
- 第 1 关代码简洁，按 (服务, 指标) 聚合，每行舍入一次（[[amz-aws-billing-stage1-invoice-in-code]]）。
- 阶梯价按边际计算，能手算 102400 GB（[[amz-aws-billing-tiered-pricing-is-marginal]]）。
- 先聚合再分档，说得出逐条分档为什么多收钱（[[amz-aws-billing-aggregate-before-tiering]]）。
- 用量按编号去重，内容冲突报错，计费代码不知道重复（[[amz-aws-billing-followup-duplicate-usage-reports]]）。
- 价格有生效时间，币种分别求和，费率类不动（[[amz-aws-billing-followup-mid-month-price-change]]）。
- 检查与写入在同一个临界区（[[amz-aws-billing-concurrency-check-then-insert-race]]）。
- 金额不用 float，不逐条分档，行与总额对得上（[[amz-aws-billing-common-mistake-float-and-per-record-tiers]]）。

**题解**：[[solution-amz-aws-billing]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
