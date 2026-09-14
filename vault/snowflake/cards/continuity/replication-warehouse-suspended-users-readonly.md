---
id: replication-warehouse-suspended-users-readonly
node: continuity.replication-and-failover
type: qa
source: snowflake-docs
---
## Q
复制到目标账户的仓库（warehouse）、用户和角色处于什么状态？在目标账户里能直接新建或修改用户吗？

## A
仓库不复制主仓库的运行状态，一律以挂起状态复制到目标账户，需要时再恢复。被复制的用户和角色在目标账户中是只读的，不能修改：必须在源账户创建或修改，再复制到各目标账户。另外，在源账户启用多因素认证（MFA）的用户，登录每个目标账户时需要重新单独注册 MFA。
