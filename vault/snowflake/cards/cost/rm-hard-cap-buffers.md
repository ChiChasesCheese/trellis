---
id: rm-hard-cap-buffers
node: cost.resource-monitors-and-budgets
type: qa
source: snowflake-docs
---
## Q
想把资源监控器（resource monitor）当作严格的支出上限，而不仅是提醒，应该怎么配置？为什么即使用 Suspend Immediately 也不能精确到单个信用点？

## A
资源监控器按周期（日、周、月等）跟踪和控制消耗，不是为精确到单个信用点或按小时严格控制设计的：达到阈值后，仓库挂起需要一些时间，即使是立即挂起也会多耗一些信用点。要严格执行配额：(1) 在阈值上留缓冲，例如在 90% 而不是 100% 触发挂起；(2) 每个监控器只分配一个仓库，因为多个仓库共享同一个配额时，一个仓库的消耗会连累其他仓库被挂起。
