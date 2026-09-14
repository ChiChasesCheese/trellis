---
id: three-layer-cloud-services-scope
node: architecture.three-layer-model
type: qa
source: snowflake-docs
---
## Q
云服务（Cloud Services）层具体管理哪些职责，它和计算层的关键区别是什么？

## A
云服务层负责安全鉴权与访问控制、查询解析与优化、事务管理、元数据管理（包括系统级的 SNOWFLAKE 数据库和 Information Schema）、基础设施与云平台对接、合规等。它自身也运行在由 Snowflake 从云厂商申请的计算实例上，但它从不直接读写表数据的字节内容——真正扫描和计算表数据是虚拟仓库（计算层）的职责，云服务层只处理围绕数据的协调工作。
