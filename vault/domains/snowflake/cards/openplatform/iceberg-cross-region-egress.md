---
id: iceberg-cross-region-egress
node: openplatform.iceberg-tables
type: qa
source: snowflake-docs
---
## Q
Snowflake 账户在 AWS us-east-1，而 Iceberg 表的外部卷放在另一个区域。这种跨区域配置可行吗？会产生哪些额外费用？

## A
可行，Snowflake 支持外部卷位于不同云或不同区域。代价是数据传输费：查询这类表时，客户的外部云存储账户会产生出口（egress）费用；对于 Snowflake 管理的 Iceberg 表，Snowflake 的跨区域/跨云写入还会以 `DATA_LAKE` 传输类型计入 Snowflake 账单（可在 DATA_TRANSFER_HISTORY 视图中查看）。因此跨区域访问频繁时，把外部卷和账户放在同一区域通常更省钱。
