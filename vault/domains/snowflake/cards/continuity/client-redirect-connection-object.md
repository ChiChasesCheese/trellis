---
id: client-redirect-connection-object
node: continuity.client-redirect
type: qa
tags: [grown]
---
## Q
Snowflake 的客户端重定向（Client Redirect）要解决什么问题？它依赖哪个对象？

## A
故障转移后数据已经可以在另一个账户读写，但应用、BI 工具和驱动程序里写死的仍是原账户的 URL，逐个改连接串既慢又容易漏。客户端重定向引入连接对象（connection）：客户端改用组织级的连接 URL，而不是某个具体账户的 URL；这个 URL 指向当前的主连接所在账户，切换时只需在 Snowflake 中改变主连接，客户端配置无需修改。
