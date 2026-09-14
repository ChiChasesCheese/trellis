---
id: share-object-what-is
node: sharing.secure-data-sharing-mechanics
type: qa
source: snowflake-docs
---
## Q
Snowflake 中的共享（share）对象是什么？提供方有哪两种方式把对象放进 share？

## A
share 是一个具名的 Snowflake 对象，封装了共享一个数据库所需的全部信息：包含哪些对象的权限、以及哪些账户可以消费。提供方可以 (1) 先把对象权限授予一个数据库角色（database role），再把该数据库角色授予 share；或 (2) 把对象权限直接授予 share；两种方式可以并用。然后把消费方账户加入 share。一个 share 可以包含同一账户下多个数据库的数据。
