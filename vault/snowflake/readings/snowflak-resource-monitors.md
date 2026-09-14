---
nodes:
- cost.resource-monitors-and-budgets
- warehouse.resource-monitors
title: 资源监控器(Resource Monitor):信用点配额与自动挂起
corpus: snowflake-docs
section: 34-resource-monitors
url: https://docs.snowflake.com/en/user-guide/resource-monitors
tags:
- canonical
---

# 资源监控器(Resource Monitor):信用点配额与自动挂起

资源监控器给账户级或若干指定仓库设定一个周期性的信用点配额(credit quota),当用量达到某个百分比阈值时可以触发三类动作:仅通知、通知并等当前语句跑完再挂起(Suspend)、或通知并立即取消正在运行的语句强制挂起(Suspend Immediately)。它只能控制用户管理的虚拟仓库,管不了 serverless 特性(如 Snowpipe、自动聚簇、物化视图维护)消耗的信用点——那些要用budget(预算)对象来监控。账户级监控器和仓库级监控器可以同时存在,任意一个先触发阈值都会生效;由于挂起动作本身需要时间生效,严格控成本时建议把阈值设在略低于 100% 的位置留出缓冲。
