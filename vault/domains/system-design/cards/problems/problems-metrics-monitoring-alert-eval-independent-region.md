---
id: problems-metrics-monitoring-alert-eval-independent-region
node: problems.search.metrics-monitoring
type: qa
step: 7
tags: [grown]
---
## Q
In a metrics monitoring and alerting system design, why must the alert-rule evaluator avoid a hard synchronous dependency on any single storage region, and what number shows the benefit of evaluating against pre-aggregated recording rules instead of raw data?

## A
The alert-evaluation path is most needed to work at exactly the moment its own infrastructure might be failing — if evaluation reads from the same storage region that just went down, the system goes silent precisely when a page is most needed. The evaluator must read from at least two independently replicated storage regions with automatic read failover, the same way the underlying write path stores each sample in two separate regions, so a single region's outage degrades read capacity in the surviving region rather than blacking out evaluation. Separately, evaluating a rule directly over 50,000 raw per-instance series at a 30-second cadence costs about 50,000/30 ≈ 1,667 series-scans/sec; pre-aggregating away the instance dimension with a continuously maintained recording rule first (down to 20 endpoints × 5 status classes = 100 series) drops this to about 100/30 ≈ 3.33 series-scans/sec — a 500x reduction, and this cost then stops scaling with fleet size.

## Q zh
在一个指标监控与告警系统设计中，为什么告警规则评估器不能对任何单一存储 region 有硬性同步依赖？用预聚合的 recording rule 而不是原始数据来评估，能带来多大的数字优势？

## A zh
告警评估路径最需要正常工作的时刻，恰恰是它自己的基础设施可能正在故障的时刻——如果评估读的是刚刚宕机的那个存储 region，系统会在最需要发声的时候恰好沉默。评估器必须从至少两个独立复制的存储 region 读取并有自动读故障切换，就像底层写路径把每个样本存进两个独立 region 一样，这样单一 region 故障只会让健康 region 的读容量吃紧，而不会让评估整体失声。另外，如果一条规则直接对 50,000 条原始的按实例分组序列以 30 秒周期现场评估，成本约为 50,000/30 ≈ 1,667 次序列扫描/秒；先用一条持续维护的 recording rule 把实例维度聚合掉（降到 20 个接口 × 5 个状态类 = 100 条序列），评估成本降到约 100/30 ≈ 3.33 次序列扫描/秒——降低 500 倍，且此后这个成本不再随主机规模增长。
