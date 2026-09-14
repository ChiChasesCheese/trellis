---
id: serverless-attribution-risk
node: cost.serverless-feature-billing
type: qa
source: snowflake-docs
---
## Q
团队只盯着各虚拟仓库的信用点消耗做成本控制，结果月度账单仍然超出预算。无服务器（serverless）计费模式可能在哪里造成盲区？

## A
无服务器功能（如 Snowpipe、无服务器 Task、搜索优化、QAS）不计入任何仓库，而是在账单上各自单独成项，所以只看仓库消耗会漏掉它们。这类功能在后台持续运行、自动扩缩，例如给大表开启搜索优化或高频写入触发持续维护，费用会在无人执行查询时悄悄增长。需要按服务类型查看消耗（如 Snowsight 成本管理页按 Service Type 筛选，或查询各功能对应的 ACCOUNT_USAGE 历史视图）。
