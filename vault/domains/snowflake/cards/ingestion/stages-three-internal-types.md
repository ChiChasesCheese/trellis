---
id: stages-three-internal-types
node: ingestion.file-formats-and-stages
type: qa
source: snowflake-docs
---
## Q
Snowflake 内部暂存区（internal stage）有用户暂存区、表暂存区、命名暂存区三种。各自的使用范围是什么？

## A
用户暂存区（user stage）：每个用户自动拥有一个，供单个用户暂存和管理文件，可加载到多张表，不能修改或删除。表暂存区（table stage）：每张表自动拥有一个，可由多个用户暂存文件，但只能加载进这一张表，同样不能修改或删除。命名暂存区（named internal stage）：在模式中显式创建的数据库对象，可由多个用户使用并加载到多张表。
