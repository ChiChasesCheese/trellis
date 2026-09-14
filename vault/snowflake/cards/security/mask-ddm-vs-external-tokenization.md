---
id: mask-ddm-vs-external-tokenization
node: security.column-masking-policies
type: qa
source: snowflake-docs
---
## Q
动态数据脱敏（Dynamic Data Masking）和外部令牌化（External Tokenization）该怎么选？各自的关键取舍是什么？

## A
外部令牌化在数据加载进 Snowflake 之前就由第三方令牌化服务把敏感值替换成令牌，查询时通过外部函数（external function）调用该服务的 REST API 去令牌化：未授权用户永远看不到真实值，且同一原值对应同一令牌，仍可按令牌分组统计（保留分析价值）；代价是依赖第三方，且外部函数不能在数据共享（data sharing）上下文中调用。动态数据脱敏以明文加载、只用 Snowflake 内置功能，支持数据共享，但脱敏后的值通常失去分组分析的价值。
