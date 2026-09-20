---
id: problems-metrics-monitoring-cardinality-not-sample-rate
node: problems.search.metrics-monitoring
type: qa
step: 1
tags: [grown]
---
## Q
In a metrics monitoring system design, a normal metric grouped by instance × endpoint × status class across 500 instances, 20 endpoints, and 5 status classes produces 50,000 time series. If someone adds a `user_id` label with 10 million distinct values to that same metric, how many series does it produce, and why does this make cardinality (the number of distinct label combinations) a far more dangerous scaling dimension than sample rate?

## A
50,000 × 10,000,000 = 5×10^11 series — a 10-million-fold increase from one added label. Sample rate is a linear cost knob: halving the scrape interval doubles ingestion cost. Cardinality is multiplicative: one unbounded label multiplies the total series count by its own distinct-value count, so a single mislabeled metric can outgrow the entire cluster's capacity in one release, while no plausible change to scrape frequency could ever do the same. This is why cardinality, not sample rate, is the dimension that has to be bounded by design rather than tuned after the fact.

## Q zh
在一个指标监控系统设计中，一个按实例 × 接口 × 状态类分组的正常指标，在 500 个实例、20 个接口、5 个状态类下产生 50,000 条时间序列。如果有人给这个指标加了一个有 1000 万个不同取值的 `user_id` 标签，会产生多少条序列？为什么这让基数（cardinality，不同标签组合的数量）比采样率危险得多？

## A zh
50,000 × 10,000,000 = 5×10^11 条序列——一个新增标签就让序列数增长了 1000 万倍。采样率是线性成本旋钮：抓取间隔减半，写入成本翻倍。基数是乘法维度：一个无界标签会把总序列数乘上它自己的不同取值数，所以一个打错标签的指标可能在一次发布里就让整个集群容量被打穿，而对抓取频率做任何合理调整都不可能造成同等后果。这就是为什么必须靠设计而不是事后调优来限制基数，而不是采样率。
