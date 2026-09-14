---
id: cleanroom-template-allowlist
node: sharing.clean-rooms-privacy
type: qa
tags: [grown]
---
## Q
数据洁净室（Data Clean Room）中，为什么由数据提供方批准“查询模板（query template）”，而不是给对方开放受限的 SELECT 权限？

## A
列级或行级权限只能限制“能读哪些数据”，限制不了“能怎么组合和计算”——拿到读权限的一方仍能逐行导出或用巧妙的过滤条件还原个体。查询模板是白名单式控制：提供方预先定义并批准允许执行的分析（连接键、可用列、必须聚合），消费方只能填参数运行，因此提供方在不暴露原始行的前提下精确控制了对方可以从数据中得出什么。
