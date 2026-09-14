---
id: dt-adaptive-definition
node: pipelines.dynamictable-adaptive-refresh
type: qa
source: snowflake-docs
---
## Q
动态表的 `REFRESH_MODE = ADAPTIVE` 是怎样工作的？它要解决增量刷新的什么问题？

## A
ADAPTIVE 默认使用增量刷新，只处理变化的行；但当检测到上游发生大规模变化时，它会自动改为重新初始化（重新计算整个结果）。增量刷新的优势建立在「变化量远小于全量」之上，一旦上游发生大批量回填或重写，逐行计算增量反而可能比从头重算更慢，ADAPTIVE 就是在这种情况下自动切换策略。
