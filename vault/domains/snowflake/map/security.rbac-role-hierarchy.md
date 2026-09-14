%% trellis:begin %%
# RBAC 角色层级
*安全与治理*

角色构成一个有向无环图（DAG，而非树），权限沿着继承关系向上流动，以及为何一个角色可以有多个父角色。

**Requires:** [[metadata.foundationdb-role|FoundationDB 作为元数据存储]]

**Unlocks:** [[security.rbac-ownership-and-grants|所有权与授权传播]], [[security.row-access-policies|行级访问策略（row access policy）]], [[security.column-masking-policies|动态数据脱敏（dynamic data masking）]], [[security.data-lineage-and-access-history|数据血缘与访问历史]], [[sharing.secure-data-sharing-mechanics|安全数据共享（Secure Data Sharing）机制]]

## Readings
- [[snowflak-access-control-rbac|访问控制总览:角色层级与 OWNERSHIP]]

## Cards (5)
- [[rbac-custom-roles-under-sysadmin]]
- [[rbac-database-roles-not-activatable]]
- [[rbac-inheritance-flows-up]]
- [[rbac-role-owner-no-inherit]]
- [[rbac-secondary-roles-create-rule]]
%% trellis:end %%

## Notes
