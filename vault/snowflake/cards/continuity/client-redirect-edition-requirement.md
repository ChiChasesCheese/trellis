---
id: client-redirect-edition-requirement
node: continuity.client-redirect
type: qa
tags: [grown]
---
## Q
一个企业版（Enterprise Edition）账户能不能用客户端重定向做跨区域的业务连续性切换？

## A
不能。客户端重定向与故障转移组一样，属于业务关键版（Business Critical Edition）或更高版本才提供的业务连续性功能。企业版可以复制数据库形成只读副本，但既不能把次级组提升为可写主组，也不能通过连接对象（connection）把客户端流量自动切换到目标账户。
