---
id: rm-suspend-vs-immediate
node: cost.resource-monitors-and-budgets
type: qa
source: snowflake-docs
---
## Q
资源监控器（resource monitor）的 Notify & Suspend 和 Notify & Suspend Immediately 两种动作有什么区别？为什么只配 Suspend 可能仍然超出配额？

## A
Suspend：发送通知，并在仓库上正在执行的语句全部完成后再挂起，期间不再接新查询。Suspend Immediately：发送通知并立即挂起，取消正在执行的语句。只配 Suspend 时，一条在阈值前开始的长查询可以在阈值触发后继续跑完，仓库在配额用尽后仍在消耗信用点。常见组合是 90% 时 Suspend、100% 时 Suspend Immediately 兜底。
