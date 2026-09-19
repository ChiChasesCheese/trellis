%% trellis:begin %%
# VARIANT 类型与存储
*半结构化数据*

JSON/Avro/Parquet/XML 如何在加载时被一次性解析，转换为同一种微分区格式内部的自描述列式表示。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/storage.micro-partition-format|微分区（micro-partition）格式]]

**Unlocks:** [[domains/snowflake/map/semistructured.schema-on-read-parsing|读时模式解析（schema-on-read）]], [[domains/snowflake/map/semistructured.flatten-lateral-joins|FLATTEN 与 LATERAL 连接]], [[domains/snowflake/map/semistructured.schema-evolution-tables|半结构化数据源上的模式演进]]

## Readings
- [[snowflak-semistructured-loading|半结构化数据的加载与内部表示(VARIANT/ARRAY/OBJECT)]]

## Cards (5)
1. [[variant-128mb-value-limit-split]]
2. [[variant-array-object-nesting-rule]]
3. [[variant-internal-optimized-format]]
4. [[variant-object-is-map-not-oop]]
5. [[variant-single-column-vs-split-columns]]
%% trellis:end %%

## Notes
