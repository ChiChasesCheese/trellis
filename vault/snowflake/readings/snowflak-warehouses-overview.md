---
nodes:
- warehouse.sizing-t-shirt
- warehouse.auto-suspend-resume
- warehouse.query-queuing
- cost.warehouse-billing-60s-minimum
title: 虚拟仓库总览:尺寸、自动挂起与排队
corpus: snowflake-docs
section: 05-warehouses-overview
url: https://docs.snowflake.com/en/user-guide/warehouses-overview
tags:
- canonical
---

# 虚拟仓库总览:尺寸、自动挂起与排队

虚拟仓库(virtual warehouse)按 T 恤码从 X-Small 到 6X-Large 分级,每上一级计算资源和每小时信用点消耗大致翻倍,但每次启动都有 60 秒最低计费,之后按秒计费。自动挂起(auto-suspend)在空闲一段时间后自动停止计费,自动恢复(auto-resume)在新查询到来时自动拉起仓库,二者都作用于整个仓库而非单个集群。当仓库现有资源不足以同时处理所有查询时,后续查询会排队等待,此时可以选择扩容仓库尺寸,或改用多集群仓库来自动增加集群数。读完能解释:仓库尺寸决定单个查询的处理速度,而不是解决并发排队的正确手段。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.snowflake.com/en/user-guide/warehouses-overview)

## Archived copy
![[snowflak-warehouses-overview-clip]]
%% trellis:end %%
