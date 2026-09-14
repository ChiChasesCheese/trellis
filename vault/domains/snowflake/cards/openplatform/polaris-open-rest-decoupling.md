---
id: polaris-open-rest-decoupling
node: openplatform.polaris-catalog
type: qa
source: snowflake-docs
---
## Q
Polaris（在 Snowflake 中以 Snowflake Open Catalog 提供的开源 Iceberg catalog）为什么采用 Iceberg REST catalog 协议？它解耦了什么？

## A
Polaris 实现了开放的 Iceberg REST catalog API，因此 Spark、Flink、Trino、Snowflake 等任何支持该协议的引擎都能通过同一个 catalog 发现、读取和写入表，不被某一家引擎的私有目录绑定。这把“哪个引擎写入了表”和“哪些引擎/主体可以查询表”分离开：写入者可以是 Spark，查询者可以是 Snowflake，访问控制集中在 catalog 中统一管理。
