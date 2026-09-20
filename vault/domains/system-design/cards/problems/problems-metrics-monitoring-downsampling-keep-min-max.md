---
id: problems-metrics-monitoring-downsampling-keep-min-max
node: problems.search.metrics-monitoring
type: qa
step: 5
tags: [grown]
---
## Q
In a metrics monitoring system's tiered downsampling design, why must a background rollup job store count/sum/min/max for each rolled-up window instead of just an average, and what storage reduction does tiering give versus keeping raw resolution forever?

## A
Storing only the average silently flattens historical spikes: months later, there is no way to tell from a 1-hour average whether a metric briefly crossed an alert threshold, because the spike and a smooth value that happens to share the same mean are indistinguishable once only the average survives. Keeping min/max/count alongside the average preserves the fact that a spike happened, even at reduced time resolution. On a worked example with 15 days of raw resolution, 90 days at a 1-minute rollup (4x reduction), and 730 days at a 1-hour rollup (240x reduction), total storage comes out to about 91.5 TB versus about 1,648 TB for keeping raw resolution for the full 730 days — roughly an 18x reduction.

## Q zh
在一个指标监控系统的分层降采样（downsampling）设计中，为什么后台 rollup 任务必须为每个滚动窗口存储 count/sum/min/max，而不是只存平均值？分层相比永久保留原始精度能带来多大的存储降低？

## A zh
只存平均值会把历史尖峰悄悄抹平：几个月后，无法从一个 1 小时平均值判断某个指标是否曾短暂越过告警阈值，因为一次真实尖峰和一个恰好均值相同的平稳值，一旦只剩下平均值就无法区分。在平均值之外同时保留 min/max/count，即使在更粗的时间精度下也能保留「确实发生过尖峰」这个事实。在一个具体算例中，15 天原始精度、90 天 1 分钟粒度滚动（降采样系数 4 倍）、730 天 1 小时粒度滚动（降采样系数 240 倍），总存储约 91.5 TB，相比把原始精度一路保留满 730 天所需的约 1,648 TB，降低约 18 倍。
