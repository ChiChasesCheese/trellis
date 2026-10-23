---
id: hl-business-strategy-lifecycle
node: company.business
type: qa
step: 10
---
## Q
一个量化交易策略从想法到上线经历哪几步？回测（backtest）是什么？

## A
1. 研究员提出假设，例如"某指标升高后，价格在 5 秒内上涨的概率更高"。
2. 用历史数据做**回测**（backtest）：重放历史行情，看按这个规则交易会怎样。
3. 通过了才上线；上线后监控、对账、再调参。

第 2 步要读海量历史数据，并重复成千上万次。这就是研究平台（research platform）、分布式存储和计算集群存在的原因：研究员迭代越快，公司的研究产出越快。
