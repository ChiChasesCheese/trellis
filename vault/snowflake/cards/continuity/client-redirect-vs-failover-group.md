---
id: client-redirect-vs-failover-group
node: continuity.client-redirect
type: qa
tags: [grown]
---
## Q
已经把故障转移组（failover group）提升为主组，为什么应用仍然连不上新的主账户里的数据？客户端重定向和故障转移组各负责什么？

## A
两者是独立的机制。故障转移组负责数据和账户对象：把次级组提升为主组，目标账户的对象变为可读写。客户端重定向负责流量：把连接对象（connection）的主连接切到目标账户，使组织级连接 URL 解析到新账户。只提升故障转移组而不切换连接，客户端仍连到旧账户；只切换连接而不提升故障转移组，客户端会连到只读的次级对象上。业务切换需要两步都做。
