%% trellis:begin %%
# 云服务（Cloud Services，GS）层
*核心架构*

这个无状态服务层做什么——身份认证、查询解析/优化、事务管理、元数据管理——但从不直接接触表的字节数据。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/snowflake/map/metadata.foundationdb-role|FoundationDB 作为元数据存储]], [[domains/snowflake/map/metadata.query-compiler-pipeline|查询编译流水线]], [[domains/snowflake/map/security.authn-mfa-sso|身份认证（MFA、SSO、密钥对）]], [[domains/snowflake/map/security.encryption-key-hierarchy|加密密钥层级]], [[domains/snowflake/map/openplatform.snowpark-udf-udtf|Snowpark 用户自定义函数（UDF）与表函数（UDTF）]]

## Readings
- [[snowflak-key-concepts-architecture|Snowflake 关键概念与整体架构]]

## Cards (5)
1. [[cloud-services-coordinates-sign-in-to-dispatch]]
2. [[cloud-services-metadata-snowflake-db-info-schema]]
3. [[cloud-services-never-reads-table-bytes]]
4. [[cloud-services-query-optimization-before-warehouse]]
5. [[cloud-services-security-centralized]]
%% trellis:end %%

## Notes
