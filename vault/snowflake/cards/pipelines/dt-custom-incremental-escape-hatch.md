---
id: dt-custom-incremental-escape-hatch
node: pipelines.dynamictable-adaptive-refresh
type: qa
source: snowflake-docs
---
## Q
如果内置的增量、全量、自适应策略都不能很好地处理某个动态表的特殊更新逻辑，还有什么选择？代价是什么？

## A
可以使用 `CUSTOM_INCREMENTAL` 模式，用 DML 语句自己定义刷新逻辑，把增量的计算方式交由用户控制。代价是失去了声明式的便利：刷新是否正确、是否高效由自己编写的 DML 负责，Snowflake 不再能自动推导增量或在大变化时自动重新初始化。它适合少数高级场景，而不是默认选择。
