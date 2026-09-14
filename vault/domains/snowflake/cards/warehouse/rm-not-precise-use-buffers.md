---
id: rm-not-precise-use-buffers
node: warehouse.resource-monitors
type: qa
source: snowflake-docs
---
## Q
要用 resource monitor（资源监控器）严格守住每个仓库的 credit（信用点）配额，为什么不能指望它精确到单个 credit 或按小时控制？应如何配置？

## A
resource monitor 是按周期（日、周、月等）追踪和控制用量的，不是按小时的精确限额：达到阈值后，即使是 Suspend Immediately，仓库也需要一些时间才能真正挂起，期间仍会继续消耗 credit。严格控制的做法：① 在阈值中留缓冲，例如设 90% 而不是 100%；② 每个 resource monitor 只分配一个仓库——多个仓库共享同一配额时，一个仓库的用量会连累其他仓库被挂起。
