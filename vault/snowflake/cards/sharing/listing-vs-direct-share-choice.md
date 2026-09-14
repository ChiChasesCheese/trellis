---
id: listing-vs-direct-share-choice
node: sharing.data-marketplace-listings
type: qa
source: snowflake-docs
---
## Q
提供方要把同一份数据给很多账户，其中一些还在其他云区域。为什么这种场景更适合用挂牌（listing）而不是直接共享（direct share）？

## A
直接共享只能把 share 给同一区域内的具名账户，逐个添加账户、不带产品描述，也不跨区域。挂牌把 share 包装成带元数据（说明、示例、条款）的数据产品，可以私下提供给指定账户或公开发布到 Snowflake Marketplace 被发现，并能由平台负责跨区域的交付；提供方还能获得消费方使用情况的指标。已有的直接共享也可以转换为挂牌。
