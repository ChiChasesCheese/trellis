---
id: fdb-commit-point
node: metadata.foundationdb-role
type: qa
tags: [grown]
---
## Q
一条 INSERT 在 Snowflake 中已经把新的微分区（micro-partition）文件写入对象存储，但在提交前云服务崩溃了。其他查询会看到这些新数据吗？为什么？

## A
不会。对象存储里的文件只有被元数据引用才属于某个表版本；提交这一步是在 FoundationDB（元数据存储）中执行的一个事务，它原子地把新文件登记为表的新版本。事务没有提交，元数据中表的文件列表就没有变化，所有查询仍按旧版本读取，写入的文件只是无人引用的孤儿文件，之后可以被清理。换言之，元数据事务就是 Snowflake 写操作真正的提交点。
