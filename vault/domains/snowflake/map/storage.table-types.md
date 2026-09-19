%% trellis:begin %%
# 表类型
*存储引擎与微分区（micro-partition）*

永久表、瞬态表（transient）、临时表（temporary）与外部表——各自享有怎样的时间旅行（Time Travel）与故障保护（Fail-safe）能力，以及原因。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/storage.micro-partition-format|微分区（micro-partition）格式]]

**Unlocks:** [[domains/snowflake/map/ingestion.bulk-copy-into|批量加载（COPY INTO）]], [[domains/snowflake/map/openplatform.hybrid-tables-oltp|混合表（Hybrid Table，Unistore）]]

## Readings
- [[snowflak-time-travel|时间旅行(Time Travel):可查询窗口、AT/BEFORE 与 UNDROP]]

## Cards (5)
1. [[table-types-choose-transient-for-staging]]
2. [[table-types-external-hybrid-clone-limits]]
3. [[table-types-min-retention-override]]
4. [[table-types-retention-ranges]]
5. [[table-types-zero-retention-permanent-vs-transient]]
%% trellis:end %%

## Notes
