---
id: dt-auto-decided-at-creation
node: pipelines.dynamictable-incremental-vs-full-refresh
type: qa
source: snowflake-docs
---
## Q
动态表用 `REFRESH_MODE = AUTO` 创建，后来发现它一直在做全量刷新。可能的原因是什么？

## A
AUTO 模式是在创建时由 Snowflake 根据查询定义是否支持增量刷新来决定模式的，而不是每次刷新时动态判断。如果定义中使用了不支持增量计算的构造，AUTO 就会在创建时选定 FULL，此后一直全量刷新。若希望使用增量刷新，需要调整查询使其支持增量，并显式指定 `INCREMENTAL` 以便在不支持时尽早报错。
