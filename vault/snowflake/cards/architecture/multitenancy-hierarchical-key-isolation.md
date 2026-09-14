---
id: multitenancy-hierarchical-key-isolation
node: architecture.elasticity-multitenancy
type: qa
tags: [grown]
---
## Q
多个 Snowflake 客户的数据都放在同一个云厂商的对象存储服务里，Snowflake 靠什么保证一个租户无法读到另一个租户的数据，并限制密钥泄露的影响范围？

## A
所有数据都加密存储，并使用分层密钥模型（hierarchical key model）：根密钥之下是每个账户的账户密钥，其下是表密钥，再下是文件密钥，上层密钥加密下层密钥。每个账户有独立的密钥分支，所以即使底层存储是共享的，缺少对应账户密钥也无法解密数据；并且单个密钥只覆盖其子树，例如一个文件密钥泄露只影响那一个文件，而不是整个账户或整个服务。
