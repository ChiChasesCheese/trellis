---
id: cloud-services-never-reads-table-bytes
node: architecture.cloud-services-layer
type: qa
source: snowflake-docs
---
## Q
Snowflake 的云服务（Cloud Services）层也跑在云厂商的计算实例上，那它和虚拟仓库（virtual warehouse）在“做什么”上的分工边界是什么？

## A
云服务层运行在 Snowflake 自己向云厂商申请的计算实例上，负责认证、访问控制、元数据、查询解析与优化等围绕数据的协调工作，但不负责扫描和计算表里的实际数据字节。读取微分区（micro-partition，表数据的存储单元）、做连接和聚合是虚拟仓库的工作。这种分工让协调逻辑与重计算解耦：用户能暂停或调整自己的仓库，而登录、权限、元数据等服务照常可用。
