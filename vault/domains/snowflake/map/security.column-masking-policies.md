%% trellis:begin %%
# 动态数据脱敏（dynamic data masking）
*安全与治理*

给列附加一个脱敏函数，使其未脱敏的原始值只对策略允许的角色可见。

**Requires:** [[domains/snowflake/map/security.rbac-role-hierarchy|RBAC 角色层级]]

**Unlocks:** [[domains/snowflake/map/security.data-classification-and-tagging|数据分类与对象标签]]

## Readings
- [[snowflak-column-masking|列级安全:动态数据脱敏(Masking Policy)]]

## Cards (6)
- [[mask-applied-everywhere-antipattern]]
- [[mask-ddm-vs-external-tokenization]]
- [[mask-leak-via-insert]]
- [[mask-policy-structure-rules]]
- [[mask-query-time-not-static]]
- [[mask-sod-vs-secure-views]]
%% trellis:end %%

## Notes
