---
id: dt-scheduler-disable-external
node: pipelines.dynamictable-target-lag
type: qa
source: snowflake-docs
---
## Q
团队已经用 Airflow 或 dbt 统一编排所有作业，希望动态表也由外部工具触发刷新，而不是由 Snowflake 按目标延迟自动调度。怎么做？

## A
为动态表设置 `SCHEDULER = DISABLE`，关闭 Snowflake 的自动调度；之后由用户手动或通过 dbt、Airflow 等外部工具触发刷新。默认情况下，Snowflake 会监控动态表、检测上游变化，并按依赖图顺序自动派发刷新。
