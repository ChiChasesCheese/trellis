---
id: problems-job-scheduler-cron-clustering-peak-multiplier
node: problems.foundations.job-scheduler
type: qa
step: 2
tags: [grown]
---
## Q
In a distributed job scheduler averaging about 1,157 trigger QPS from 10^8 jobs/day, why would the design use a higher peak multiplier (around 6x) than the 3-4x commonly used for organic user traffic, and what does this reveal about scheduled workloads specifically?

## A
Unlike organic user traffic, which tends to spread smoothly across the day with only moderate diurnal peaks, scheduled job due times are not uniformly distributed -- large numbers of jobs get configured to fire at shared boundaries like the top of the hour or midnight, so actual due-time load spikes well above what a uniform-distribution average would suggest. This reveals that scheduled workloads have a structural clustering problem baked into how users configure schedules, which is also the root cause the multi-tenant fairness mechanism (per-tenant rate limiting and weighted dispatch) has to address, since one tenant's boundary-aligned burst can otherwise crowd out every other tenant's on-time triggering at that same moment.

## Q zh
在一个每天 10^8 个任务、平均触发 QPS 约 1,157 的分布式任务调度器里，为什么设计会采用比普通用户流量常见的 3-4 倍更高的峰值系数（约 6 倍）？这揭示了调度类工作负载的什么特殊性？

## A zh
不同于通常在一天内相对平滑分布、只有中等日间峰值的自然用户流量，调度任务的到期时间并不是均匀分布的——大量任务被配置成在整点、午夜这类共享的时间边界上触发，导致真实到期负载的尖峰远高于均匀分布假设下的估计。这揭示了调度类负载天生带有一种结构性的扎堆问题，根源来自用户配置调度的方式本身——这也正是多租户公平机制（按租户限流和加权分发）必须处理的根本原因，因为一个租户在这些边界上的突发流量如果不加控制，会挤占同一时刻其他所有租户本该准时触发的任务。
