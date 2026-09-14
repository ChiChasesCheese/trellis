---
id: share-read-only-consumer-db
node: sharing.secure-data-sharing-mechanics
type: qa
source: snowflake-docs
---
## Q
消费方从一个共享（share）创建数据库后，能对其中的表做 INSERT、UPDATE 或删除对象吗？消费方内部怎样控制谁能查询这个库？

## A
不能。账户之间共享的所有数据库对象都是只读的，不能修改或删除，也不能添加或修改表数据。消费方从 share 创建出一个只读数据库，内部访问控制仍使用标准的基于角色的访问控制（RBAC）来决定哪些角色能访问。每个 share 在消费方账户里只能创建一个数据库。
