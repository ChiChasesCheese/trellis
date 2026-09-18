%% trellis:begin %%
# 表类型
*存储引擎与微分区（micro-partition）*

永久表、瞬态表（transient）、临时表（temporary）与外部表——各自享有怎样的时间旅行（Time Travel）与故障保护（Fail-safe）能力，以及原因。

**Requires:** [[domains/snowflake/map/storage.micro-partition-format|微分区（micro-partition）格式]]

**Unlocks:** [[domains/snowflake/map/ingestion.bulk-copy-into|批量加载（COPY INTO）]], [[domains/snowflake/map/openplatform.hybrid-tables-oltp|混合表（Hybrid Table，Unistore）]]

## Readings
- [[snowflak-time-travel|时间旅行(Time Travel):可查询窗口、AT/BEFORE 与 UNDROP]]

## Cards (5)
- [[table-types-choose-transient-for-staging]]
- [[table-types-external-hybrid-clone-limits]]
- [[table-types-min-retention-override]]
- [[table-types-retention-ranges]]
- [[table-types-zero-retention-permanent-vs-transient]]
%% trellis:end %%

## Notes
