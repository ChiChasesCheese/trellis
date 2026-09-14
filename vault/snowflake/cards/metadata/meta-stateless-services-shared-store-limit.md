---
id: meta-stateless-services-shared-store-limit
node: metadata.metadata-scaling-consistency
type: qa
tags: [grown]
---
## Q
Snowflake 的云服务（Cloud Services）实例是无状态、可水平扩展的，那么在元数据路径上真正限制伸缩的是什么？它为强一致性付出了什么？

## A
限制在于所有实例共用的元数据存储：编译时读取表版本与分区列表、提交时写入新版本，全都经过它。云服务实例可以随负载增减，但元数据存储必须在分布式、跨可用区复制的情况下保证事务的强一致（可串行化），每次提交都要在多个副本间达成一致，这带来额外的提交延迟，并让写冲突以等待或重试的形式出现。
