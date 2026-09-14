---
id: compiler-cascades-no-indexes
node: metadata.query-compiler-pipeline
type: qa
tags: [grown]
---
## Q
Snowflake 的查询优化器采用什么风格？为什么它的计划搜索空间比传统带索引的数据库更小？

## A
它是 Cascades 风格、自顶向下、基于代价（cost-based）的优化器，所用统计信息在数据加载和更新时自动维护。Snowflake 表没有用户定义的二级索引，优化器不需要在“走哪个索引、索引还是全扫”之间枚举大量方案，搜索空间因此更小；此外一些决策（例如连接时的数据分布方式）被推迟到执行时再定，进一步减少了编译期要做的选择，降低了因估算错误而选出坏计划的风险。
