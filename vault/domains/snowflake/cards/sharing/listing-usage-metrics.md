---
id: listing-usage-metrics
node: sharing.data-marketplace-listings
type: qa
source: snowflake-docs
---
## Q
数据提供方想知道哪些消费方账户在用自己的数据、用得多不多。直接共享（direct share）和挂牌（listing）在这一点上有何区别？

## A
通过挂牌提供数据时（私下挂牌、Data Exchange 或 Snowflake Marketplace），提供方可以获取消费方对挂牌的使用指标以及访问挂牌的消费方账户信息；Data Exchange 中挂牌的使用数据只在导入的 SNOWFLAKE 数据库的 Data Sharing Usage 模式视图中提供。直接共享没有这种面向数据产品的使用分析，这也是把直接共享转为挂牌的常见理由之一。
