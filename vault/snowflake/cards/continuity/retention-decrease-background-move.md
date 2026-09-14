---
id: retention-decrease-background-move
node: continuity.retention-vs-failsafe
type: qa
source: snowflake-docs
---
## Q
把一张表的保留期从 10 天改成 1 天后，第 2 到第 10 天的历史数据会立刻不可访问吗？反过来从 10 天改为 20 天，已经进入故障保护（Fail-safe）的数据会回来吗？

## A
缩短时，第 2–10 天的数据会被转入故障保护，但由后台进程完成，Snowflake 保证会移动却不保证何时完成，完成前这些数据仍可通过时间旅行（Time Travel）访问。延长时，仍在时间旅行中的数据会按新的更长期限保留，但已经超过旧期限、进入故障保护的数据不会回来。
