---
id: anchor-state-in-shared-metadata
node: metadata.execution-anchor
type: qa
tags: [grown]
---
## Q
为什么执行锚点（execution anchor）实例崩溃后，其他云服务（Cloud Services）实例仍有可能接管其查询，而不是必然让客户端报错？

## A
因为查询的关键状态（查询 ID、所属会话、执行进度、事务状态）与锚点归属本身都记录在共享的强一致元数据存储中，而不是只存在于该实例的内存里。接管实例可以从元数据读出查询处于哪个阶段，据此决定继续跟踪、重新执行还是标记失败。若状态只放在单个实例的内存中，实例一挂查询就只能丢失。
