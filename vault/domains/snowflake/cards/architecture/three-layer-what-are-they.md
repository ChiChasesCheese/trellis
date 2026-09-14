---
id: three-layer-what-are-they
node: architecture.three-layer-model
type: qa
source: snowflake-docs
---
## Q
Snowflake 的三层架构分别是哪三层，它们之间通过什么相互通信？

## A
三层是：数据库存储层（存放列式压缩数据）、虚拟仓库（virtual warehouse，计算层，负责执行 SQL）、云服务层（Cloud Services，负责鉴权、查询解析优化、事务与元数据管理）。三层在物理和逻辑上彼此独立部署，互相之间只通过元数据（metadata）通信——计算层从不直接与其他计算层共享内存或磁盘，云服务层也从不直接触碰表的字节数据。
