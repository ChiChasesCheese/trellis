---
id: listing-public-vs-private
node: sharing.data-marketplace-listings
type: qa
source: snowflake-docs
---
## Q
Snowflake Marketplace 上的公开挂牌（public listing）和私有挂牌（private listing）分别适用于什么场景？付费挂牌的数据会被复制给购买方吗？

## A
公开挂牌发布在 Marketplace 上，任何 Snowflake 客户都能发现并获取（可免费、可付费或需申请），适合面向市场的数据产品；私有挂牌只提供给指定账户，适合合作伙伴或内部跨账户分发，同时保留挂牌的元数据和使用指标。无论免费还是付费，挂牌底层仍是安全数据共享（Secure Data Sharing）：同区域内不复制数据，消费方读取实时数据，只为自己的查询计算付费。
