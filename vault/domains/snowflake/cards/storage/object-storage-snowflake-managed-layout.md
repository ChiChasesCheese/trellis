---
id: object-storage-snowflake-managed-layout
node: storage.object-storage-backend
type: qa
source: snowflake-docs
---
## Q
数据加载进普通 Snowflake 表后，物理上存放在哪里？用户对这些文件能控制什么？

## A
Snowflake 把数据重组为内部优化的压缩列式格式，存放在其所在公有云的云存储中。数据的组织方式、文件大小、结构、压缩、元数据与统计信息全部由 Snowflake 管理，用户既不挑选硬件，也不直接管理这些文件，只通过 SQL 访问表。这让 Snowflake 可以自由地重写、切分和优化文件布局，而不会破坏任何用户侧依赖。
