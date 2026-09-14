---
id: fdb-what-is-stored
node: metadata.foundationdb-role
type: cloze
tags: [grown]
---
Snowflake 存放在 FoundationDB（分布式事务型 KV 存储）中的元数据包括：数据库/schema/表等 {{c1::目录对象定义}}；每个表版本由哪些 {{c2::微分区（micro-partition）文件}} 组成及各分区的统计信息；{{c3::事务状态与锁}}；以及用户、角色与权限授予等 {{c4::访问控制信息}}。表的字节数据本身不在其中，而是在云对象存储里。
