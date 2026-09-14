---
id: client-redirect-failover-steps
node: continuity.client-redirect
type: cloze
tags: [grown]
---
配置并执行客户端重定向的步骤：
1. 在源账户 {{c1::`CREATE CONNECTION`}} 创建主连接；
2. 用 {{c2::`ALTER CONNECTION … ENABLE FAILOVER TO ACCOUNTS`}} 允许目标账户；
3. 在目标账户基于主连接创建次级连接（secondary connection）；
4. 故障时在目标账户执行 {{c3::`ALTER CONNECTION … PRIMARY`}}，把它提升为主连接，连接 URL 随之指向目标账户。
