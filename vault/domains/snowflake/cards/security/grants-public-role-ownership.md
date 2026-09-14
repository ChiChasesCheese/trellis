---
id: grants-public-role-ownership
node: security.rbac-ownership-and-grants
type: qa
source: snowflake-docs
---
## Q
如果一个对象的所有者是 PUBLIC 角色，会产生什么后果？在什么场景下这是可接受的？

## A
PUBLIC 是自动授予给账户里每个用户和每个角色的伪角色（pseudo-role）。它可以像其他角色一样拥有对象，但由定义可知，PUBLIC 拥有的对象对账户内所有用户和角色都可用——相当于放弃了访问控制。只适合不需要显式访问控制、所有用户访问权对等的场景；存放敏感数据的对象若误归 PUBLIC 所有，等于对全账户公开。
