---
id: dt-cost-categories
node: pipelines.dynamictable-target-lag
type: qa
source: snowflake-docs
---
## Q
把一张动态表的 `TARGET_LAG` 从 1 小时改成 1 分钟，哪些成本会上升？

## A
动态表有三类成本：1) 仓库计算：执行每次刷新查询，刷新越频繁消耗越多；2) 云服务：编译刷新查询、追踪依赖、监控变化和协调刷新，目标延迟越短调度工作越多；3) 存储：每次刷新都会新增、替换或删除微分区（micro-partition），刷新次数和时间旅行（Time Travel）保留期都会影响存储量。缩短目标延迟会同时推高这三项。
