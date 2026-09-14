---
id: rm-cloud-services-counted
node: warehouse.resource-monitors
type: qa
source: snowflake-docs
---
## Q
resource monitor（资源监控器）配额 1000 credit，某周期内仓库本身只用了 700 credit，却触发了告警。为什么？

## A
配额同时计入用户虚拟仓库的 credit 和支撑这些仓库的云服务（cloud services）所消耗的 credit，这里云服务用了 300，合计达到 1000。并且计算时不考虑云服务每日 10% 的免费调整：即使这部分云服务用量最终不会计费，也会被算进是否达到阈值。另外，仓库级 resource monitor 只能监控、不能挂起云服务用量——仓库被挂起后，继续发往该仓库的查询仍可能产生云服务费用。
