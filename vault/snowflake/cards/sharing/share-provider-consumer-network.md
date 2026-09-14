---
id: share-provider-consumer-network
node: sharing.secure-data-sharing-mechanics
type: qa
source: snowflake-docs
---
## Q
在 Snowflake 数据共享中，提供方（provider）与消费方（consumer）的角色是固定的吗？共享能跨越 Snowflake 之外吗？

## A
不是固定的：任何完整的 Snowflake 账户都可以同时作为提供方创建 share、又作为消费方导入别人的 share，由此形成一个多对多的共享网络，也可以在同一组织的多个账户之间共享。但数据共享只支持 Snowflake 账户之间进行；对方没有 Snowflake 账户时，需要提供方为其创建只读账户（reader account）。
