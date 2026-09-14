---
id: sos-maintenance-background-cost
node: pruning.search-optimization-service
type: qa
source: snowflake-docs
---
## Q
为某张表启用搜索优化后，搜索访问路径是立刻可用的吗？维护过程需要用户自己创建虚拟仓库（warehouse）来跑吗？这个过程有没有额外成本？

## A
不是立刻可用的：后台的维护服务需要先构建搜索访问路径，构建耗时取决于表的大小，在构建完成之前查询不会被加速；期间不会阻塞对表的其他操作。维护过程完全对用户透明，不需要用户创建或指定虚拟仓库来运行它，但会产生额外的存储和计算资源成本，这些成本由 Snowflake 后台的维护服务本身消耗，需要用户自行评估是否值得。
