---
id: grants-future-grants
node: security.rbac-ownership-and-grants
type: qa
source: snowflake-docs
---
## Q
给角色 REPORTING 执行了 `GRANT SELECT ON ALL TABLES IN SCHEMA s`，第二天 ETL 新建的表 REPORTING 却查不了。为什么？应该用什么机制？

## A
对已存在的对象，权限必须逐个对象授予；`ALL TABLES` 只作用于执行授权那一刻已存在的表，之后新建的表不会自动获得。要让将来新建的对象自动带上初始权限，需要使用未来授权（future grant），例如 `GRANT SELECT ON FUTURE TABLES IN SCHEMA s TO ROLE REPORTING`，它定义在该模式中新建对象时自动附加的权限。在托管访问模式里，future grant 也只能由模式所有者或 MANAGE GRANTS 角色设置。
