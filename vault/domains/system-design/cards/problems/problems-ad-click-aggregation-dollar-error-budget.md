---
id: problems-ad-click-aggregation-dollar-error-budget
node: problems.search.ad-click-aggregation
type: qa
step: 1
tags: [grown]
---
## Q
In an ad click aggregation design billing on 500 million clicks/day at an average CPC (cost per click) of $0.35, why does even a tiny relative accuracy target like 0.01% translate into a design requirement, not just a nice-to-have?

## A
Daily ad spend is `5e8 * 0.35 = $175,000,000`. A 0.01% (1e-4) error rate against that spend is `175,000,000 * 0.0001 = $17,500` per day — a concrete dollar figure that would appear in an incident report, not an abstract rounding error. This is why click aggregation cannot tolerate the kind of bounded-but-nonzero error that a heavy-hitters/Top-K design accepts in exchange for bounded memory: the same 'small percentage error' that's harmless when ranking trending content becomes a specific, auditable sum of money when it's attached to billing.

## Q zh
在一个日均 5 亿次点击、平均 CPC（每次点击成本）$0.35 的广告点击聚合计费设计中，为什么哪怕 0.01% 这么小的准确率目标也会变成一条设计约束，而不只是锦上添花？

## A zh
日均广告花费是 `5e8 * 0.35 = $175,000,000`。对这笔花费而言 0.01%（1e-4）的误差率对应 `175,000,000 * 0.0001 = $17,500`/天——这是一个会出现在事故报告里的具体数字，不是抽象的舍入误差。这就是为什么点击聚合不能像 Top-K/热门内容这类设计那样，为了换取有界内存而接受「有界但非零」的误差：同样一个「百分之几的小误差」，在给内容排名时无关紧要，一旦挂上计费，就变成一笔具体的、需要审计的钱。
