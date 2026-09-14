---
id: rm-resume-conditions
node: cost.resource-monitors-and-budgets
type: qa
source: snowflake-docs
---
## Q
仓库被资源监控器（resource monitor）的挂起动作挂起后，用户手动 RESUME 却不起作用。满足什么条件后仓库才能重新恢复？

## A
被监控器挂起的仓库在以下任一条件满足前无法恢复：下一个周期开始（按监控器起始日期计算，重置时间统一是 UTC 零点）；监控器的信用点配额被调高；挂起动作的阈值被调高；仓库不再分配给该监控器；监控器被删除。这是它能作为真正上限的原因：普通用户无法绕过，只有持有相应权限的管理员修改监控器才能解除。
