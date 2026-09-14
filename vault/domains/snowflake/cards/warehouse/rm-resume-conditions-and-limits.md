---
id: rm-resume-conditions-and-limits
node: warehouse.resource-monitors
type: cloze
source: snowflake-docs
---
被 resource monitor（资源监控器）挂起的标准仓库，只有在以下情况之一发生后才能恢复：{{c1::下一个监控周期开始}}、提高监控器的 credit 配额、{{c2::提高挂起动作的阈值}}、把仓库从监控器上移除，或 {{c3::删除监控器}}。每个监控器最多 1 个 Suspend、1 个 Suspend Immediate 和 {{c4::5}} 个 Notify 动作，已用额度在周期边界的 {{c5::UTC 零点}} 重置。
