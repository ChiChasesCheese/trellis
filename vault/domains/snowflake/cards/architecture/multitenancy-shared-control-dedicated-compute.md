---
id: multitenancy-shared-control-dedicated-compute
node: architecture.elasticity-multitenancy
type: qa
tags: [grown]
---
## Q
在 Snowflake 的多租户（multi-tenancy）设计中，哪一部分是众多客户共享的，哪一部分是每个客户独占的？为什么这样划分？

## A
云服务（Cloud Services）层是重度多租户的：认证、优化、事务与元数据等服务长期运行，由大量账户共享，以摊薄成本并便于统一运维。虚拟仓库（virtual warehouse）的计算节点则不在仓库之间共享，更不跨账户共享，每条查询只在一个仓库上执行。这样一个租户的重查询不会抢占另一个租户的 CPU、内存和本地缓存，获得强性能隔离；代价是节点利用率不如混用节点的方案高。
