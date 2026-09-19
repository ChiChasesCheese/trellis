%% trellis:begin %%
# RBAC 角色层级
*安全与治理*

角色构成一个有向无环图（DAG，而非树），权限沿着继承关系向上流动，以及为何一个角色可以有多个父角色。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/metadata.foundationdb-role|FoundationDB 作为元数据存储]]

**Unlocks:** [[domains/snowflake/map/security.rbac-ownership-and-grants|所有权与授权传播]], [[domains/snowflake/map/security.row-access-policies|行级访问策略（row access policy）]], [[domains/snowflake/map/security.column-masking-policies|动态数据脱敏（dynamic data masking）]], [[domains/snowflake/map/security.data-lineage-and-access-history|数据血缘与访问历史]], [[domains/snowflake/map/sharing.secure-data-sharing-mechanics|安全数据共享（Secure Data Sharing）机制]]

## Readings
- [[snowflak-access-control-rbac|访问控制总览:角色层级与 OWNERSHIP]]

## Cards (5)
1. [[rbac-custom-roles-under-sysadmin]]
2. [[rbac-database-roles-not-activatable]]
3. [[rbac-inheritance-flows-up]]
4. [[rbac-role-owner-no-inherit]]
5. [[rbac-secondary-roles-create-rule]]
%% trellis:end %%

## Notes
