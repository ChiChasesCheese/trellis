---
id: hybrid-constraints-enforced
node: openplatform.hybrid-tables-oltp
type: qa
source: snowflake-docs
---
## Q
在 Snowflake 标准表上声明 PRIMARY KEY 和 FOREIGN KEY，插入重复主键会报错吗？换成混合表（hybrid table）呢？为什么事务型负载需要后者？

## A
标准表上 PRIMARY KEY、FOREIGN KEY、UNIQUE 都是可选且不强制执行的（只是元数据声明，只有 NOT NULL 强制），重复主键可以插入。混合表必须定义主键，且主键、唯一约束和外键（引用完整性）都被强制执行，违反即报错，并且不能对这些约束设置 NOT ENFORCED。事务型应用依赖数据库保证唯一性和引用完整性，否则就要在应用层自行查重、极易在并发下出错。
