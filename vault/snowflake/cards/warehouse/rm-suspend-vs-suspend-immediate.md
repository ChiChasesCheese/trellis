---
id: rm-suspend-vs-suspend-immediate
node: warehouse.resource-monitors
type: qa
source: snowflake-docs
---
## Q
resource monitor（资源监控器）的 Suspend 与 Suspend Immediately 两种动作有什么区别？为什么只配 100% 的 Suspend 仍可能超出配额？

## A
Suspend：发送通知，并在仓库上正在执行的语句全部完成后才挂起所分配的标准仓库，期间不再接新查询。Suspend Immediately：发送通知并立即挂起，取消所有正在执行的语句。只配 100% 的 Suspend 时，阈值前开始的长查询会在阈值后继续跑完，仓库继续消耗 credit（信用点），所以实际用量会超过配额。常见做法是 90% 设 Suspend、100% 设 Suspend Immediately（阈值也允许超过 100）。
