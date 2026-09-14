---
id: dt-refresh-modes-cloze
node: pipelines.dynamictable-incremental-vs-full-refresh
type: cloze
source: snowflake-docs
---
动态表的 `REFRESH_MODE`：{{c1::`INCREMENTAL`}} 只处理自上次刷新以来变化的行；{{c2::`FULL`}} 每次重算整个结果集；{{c3::`AUTO`}} 在创建时根据定义是否支持增量刷新由 Snowflake 选择；{{c4::`ADAPTIVE`}} 默认增量，检测到大量上游变化时自动重新初始化；{{c5::`CUSTOM_INCREMENTAL`}} 允许用 DML 语句自定义刷新逻辑。
