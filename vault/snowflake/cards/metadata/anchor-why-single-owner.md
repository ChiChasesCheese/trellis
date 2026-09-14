---
id: anchor-why-single-owner
node: metadata.execution-anchor
type: qa
tags: [grown]
---
## Q
Snowflake 的云服务（Cloud Services）有很多无状态实例，为什么一条查询在生命周期内仍要绑定到唯一一个实例，即执行锚点（execution anchor）？

## A
查询从编译、向虚拟仓库（virtual warehouse）调度执行、跟踪进度到最终提交元数据，需要一个唯一的协调者。如果两个实例同时认为自己拥有这条查询，就可能重复调度执行，甚至把同一次写入提交两次。把查询锚定到一个实例上，就明确了谁有权推进和提交这条查询；其他实例收到关于这条查询的请求（例如客户端轮询状态）时，只需找到锚点实例或读取共享元数据中的状态。
