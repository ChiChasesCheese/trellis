---
nodes:
- security.rbac-role-hierarchy
- security.rbac-ownership-and-grants
title: 访问控制总览:角色层级与 OWNERSHIP
corpus: snowflake-docs
section: 24-security-access-control-overview
url: https://docs.snowflake.com/en/user-guide/security-access-control-overview
tags:
- canonical
---

# 访问控制总览:角色层级与 OWNERSHIP

Snowflake 的访问控制融合了自主访问控制(DAC,对象归属于某个角色)、基于角色的访问控制(RBAC,权限授予角色再授予用户)和基于用户的访问控制(UBAC,权限直接授予用户)。角色可以被授予给其他角色,形成层级(role hierarchy)——权限沿层级向上传递,一个角色可以有多个“父角色”,因此层级本质上是一张有向图而非单纯的树。OWNERSHIP 是最特殊的权限:默认拥有该对象上的全部权限,并能决定把其他权限授予(GRANT)或收回(REVOKE)给谁;未来授权(future grant)可以预先为某个 schema 里“将来创建的对象”定义好默认权限。读完应能区分主角色与副角色在会话中各自的授权范围。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.snowflake.com/en/user-guide/security-access-control-overview)

## Archived copy
![[snowflak-access-control-rbac-clip]]
%% trellis:end %%
