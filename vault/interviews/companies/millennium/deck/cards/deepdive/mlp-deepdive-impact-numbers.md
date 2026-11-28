---
id: mlp-deepdive-impact-numbers
node: deepdive.impact
type: qa
step: 1
---
## Q
**用数字说结果**｜项目深挖

“What was the impact? Give me numbers.”

## A
每个项目只背几个数字，并且带着口径说。数字说不准时说量级，面试官查口径时不要被抓住。

- **Amex 管线：** 一年几千万笔交易、数十亿美元；18 个月生产；最大单个 PR 约 1,800 行。金额口径是量级，不报精确值。
- **interchange 切换：** 约 13.7M 行；字段一致率超过 99.9%；记录数差 +0.224%。这是两个性质不同的数字：一个是字段一致率，一个是记录数差异，不要混用。
- **质检框架：** 框架 PR 约 1,500 行；铺开 8 个数据域；影响面 35,000 个商户、约 50 个坏商户。
- **Quant-Stroller：** 66K 多行（含测试）、470 多个测试文件、340 多个实验、约 2,300 个因子、9 个数据商、5,500 只股票；超额夏普约 1.39（扣 10 个基点成本）。
- **净额结算：** 项目层面约 $450M 每月的垫付，是业务数字，不是你的管线产出。

**英文答法。**
- The Amex pipeline handles **tens of millions** of transactions and **billions of dollars** a year, on **eighteen months** in production.
- The interchange switch: **over 99.9%** field-level parity, and **13.7 million rows** within a fraction of a percent.
- Quant-Stroller: **340-plus experiments** in an append-only ledger, and one strategy at **excess Sharpe about 1.39** net of 10 basis points.
- The **$450M a month** is the program's float, not my pipeline's output.

**追问。**
- **What is the dollar volume exactly?** I quote the order of magnitude, billions.
- **Is it a zero-regression migration?** I say shipped dark, enabled in pre-prod, then production.
