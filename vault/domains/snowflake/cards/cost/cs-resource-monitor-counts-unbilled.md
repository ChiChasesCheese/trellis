---
id: cs-resource-monitor-counts-unbilled
node: cost.cloud-services-free-tier
type: qa
source: snowflake-docs
---
## Q
资源监控器（resource monitor）的配额是 1000 credit，仓库用了 700 credit、支撑这些仓库的云服务用了 300 credit，其中大部分云服务因为 10% 调整实际没有计费。监控器会认为达到配额吗？

## A
会。资源监控器判断是否达到配额时，把支撑这些仓库的云服务全部消耗计算在内，不考虑每日 10% 调整，即使那部分消耗最终没有出现在账单上。因此监控器统计的“已用信用点”可能高于实际计费金额，设置阈值时要考虑这一差异。
