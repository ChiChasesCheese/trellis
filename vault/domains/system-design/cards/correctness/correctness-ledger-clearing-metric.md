---
id: correctness-ledger-clearing-metric
node: correctness.ledger
type: qa
---
## Q
A double-entry ledger mirrors many independent payment systems (Stripe-style). Beyond running reconciliation jobs, what does it mean to make discrepancy detection a *first-class metric* — what does a "clearing" score measure, and why publish it as a number teams are held to?

## A
- Model each fund flow so that **intermediate ("clearing") accounts must return to zero at steady state** — money sitting in a pipe that should have drained is, by construction, a detected problem, whether the cause is lost money or just bad data mapping.
- The **clearing/data-quality score** = the fraction of ledger balances that are properly zeroed out or explained (e.g. 99.99%). One number summarizes correctness across thousands of flows, so a regression anywhere drags a visible metric.
- Publishing it turns correctness into an **SLO** (service-level objective — a measured target with an owner): teams get scored and must investigate and clear discrepancies, instead of assuming upstream systems are right. That is the "trust but verify" loop — the ledger never trusts its producers; it continuously proves them.

## Q zh
一个 double-entry ledger（复式记账账本）镜像了许多独立的支付系统（Stripe 风格）。除了跑对账任务之外，把差异检测做成*一等公民指标*是什么意思 — "clearing" 分数衡量什么？为什么要把它发布成一个团队要背的数字？

## A zh
- 对每条资金流建模，使**中间（"clearing"）账户在稳态下必须归零** — 本该流走却滞留在管道里的钱，从构造上就是一个被检测到的问题，无论原因是真丢了钱还是数据映射错了。
- **clearing / 数据质量分数** = 账本中正确归零或可解释的余额占比（例如 99.99%）。一个数字汇总了数千条资金流的正确性，任何地方的回归都会拖动一个看得见的指标。
- 发布这个数字把正确性变成 **SLO**（service-level objective，有归属人的可测目标）：团队被打分，必须调查并清掉差异，而不是默认上游系统是对的。这就是 "trust but verify" 循环 — 账本从不信任它的生产者，而是持续地证明它们。
