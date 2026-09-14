---
id: clone-grants-not-copied
node: continuity.zero-copy-clone
type: qa
source: snowflake-docs
---
## Q
用 `CREATE TABLE t_dev CLONE t_prod` 克隆一张表后，原来能读 `t_prod` 的角色能直接读 `t_dev` 吗？克隆整个数据库时又如何？

## A
单独克隆表时，大多数 `CREATE … CLONE` 不复制源对象上的授权，需要手动 GRANT，或在 CREATE TABLE … CLONE 上加 `COPY GRANTS`，复制除 OWNERSHIP 以外的所有权限。克隆数据库或模式时，其中各子对象（表、视图等）的克隆会继承源子对象上的授权，但数据库或模式这个容器本身的克隆不继承源容器上的授权。
