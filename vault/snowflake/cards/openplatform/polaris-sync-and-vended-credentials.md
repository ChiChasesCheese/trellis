---
id: polaris-sync-and-vended-credentials
node: openplatform.polaris-catalog
type: qa
source: snowflake-docs
---
## Q
一张 Snowflake 管理的 Iceberg 表需要让第三方引擎读取；另一张表由 Open Catalog（Polaris）管理，需要让 Snowflake 查询或写入。两种方向分别怎样接通？catalog 下发凭证（catalog-vended credentials）起什么作用？

## A
两个方向都通过 catalog integration（账户级对象，记录外部 catalog 中元数据如何组织）：(1) 把 Snowflake 管理的表同步（sync）到 Open Catalog，第三方引擎通过 Open Catalog 访问；(2) 让 Snowflake 通过 catalog integration 查询或写入 Open Catalog 管理的表。使用外部 catalog 时支持 catalog 下发凭证：由 catalog 为引擎签发访问底层存储的临时凭证，引擎不必各自长期持有存储密钥，存储访问权限随 catalog 授权一起集中控制。
