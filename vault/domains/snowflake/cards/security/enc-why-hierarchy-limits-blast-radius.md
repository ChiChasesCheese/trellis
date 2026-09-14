---
id: enc-why-hierarchy-limits-blast-radius
node: security.encryption-key-hierarchy
type: qa
tags: [grown]
---
## Q
为什么 Snowflake 不用一把大密钥加密所有客户的所有数据，而要做“根 → 账户 → 表 → 文件”的分层密钥结构？

## A
分层让每把密钥只保护一小块数据，缩小爆炸半径（blast radius）：一个文件密钥泄露只影响一个文件，一个账户的密钥与其他账户完全隔离，满足多租户之间的密钥隔离。同时上层密钥只包装下层密钥而不直接加密大批数据，因此轮换上层密钥只需重新包装少量密钥材料，而不必重写海量数据文件；最顶层的根密钥留在 HSM 里，从不以明文离开。
