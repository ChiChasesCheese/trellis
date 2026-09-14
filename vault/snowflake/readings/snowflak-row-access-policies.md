---
nodes:
- security.row-access-policies
title: 行访问策略(Row Access Policy):按角色过滤行
corpus: snowflake-docs
section: 25-security-row-intro
url: https://docs.snowflake.com/en/user-guide/security-row-intro
tags:
- canonical
---

# 行访问策略(Row Access Policy):按角色过滤行

行访问策略是挂在表或视图上的一段谓词表达式,在查询运行时把结果集过滤成只剩策略允许当前角色看到的那些行,对象所有者(OWNERSHIP 持有者)本该拥有全部数据的默认权限,也同样受该策略约束——这正是它能实现职责分离(segregation of duties)的关键。策略求值使用的是策略所有者的角色而非发起查询的用户角色,因此调用者不需要对策略里引用的映射表(mapping table)有权限。策略可以嵌套在表和其上的视图之间,按“表策略先于视图策略”的顺序依次生效。简单的基于 CURRENT_ROLE 判断的策略性能开销很小,涉及映射表查找的策略则会显著拖慢诸如 COUNT(*) 这类原本可以纯元数据回答的查询。
