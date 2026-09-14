%% trellis:begin %%
# VARIANT 类型与存储
*半结构化数据*

JSON/Avro/Parquet/XML 如何在加载时被一次性解析，转换为同一种微分区格式内部的自描述列式表示。

**Requires:** [[storage.micro-partition-format|微分区（micro-partition）格式]]

**Unlocks:** [[semistructured.schema-on-read-parsing|读时模式解析（schema-on-read）]], [[semistructured.flatten-lateral-joins|FLATTEN 与 LATERAL 连接]], [[semistructured.schema-evolution-tables|半结构化数据源上的模式演进]]

## Readings
- [[snowflak-semistructured-loading|半结构化数据的加载与内部表示(VARIANT/ARRAY/OBJECT)]]

## Cards (5)
- [[variant-128mb-value-limit-split]]
- [[variant-array-object-nesting-rule]]
- [[variant-internal-optimized-format]]
- [[variant-object-is-map-not-oop]]
- [[variant-single-column-vs-split-columns]]
%% trellis:end %%

## Notes
