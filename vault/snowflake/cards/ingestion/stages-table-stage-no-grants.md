---
id: stages-table-stage-no-grants
node: ingestion.file-formats-and-stages
type: qa
source: snowflake-docs
---
## Q
数据团队想让多个不拥有目标表的 ETL 角色都能往暂存区上传文件，并用权限精细控制。为什么表暂存区（table stage）做不到，应该用什么？

## A
表暂存区不是独立的数据库对象，而是隐式绑定在表上的暂存区，本身没有可授予的权限；要向它上传、列出、查询或删除文件，必须是表的所有者（拥有表 OWNERSHIP 权限的角色）。应该改用命名暂存区（named stage）：它是模式中的数据库对象，创建、修改、使用、删除都可以通过访问控制权限授予给不同角色。
