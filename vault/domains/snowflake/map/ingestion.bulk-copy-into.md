%% trellis:begin %%
# 批量加载（COPY INTO）
*数据加载与摄取*

从暂存区（stage）批量加载文件、防止同一文件被重复加载的加载元数据，以及跨文件的并行加载。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/storage.table-types|表类型]]

**Unlocks:** [[domains/snowflake/map/ingestion.file-formats-and-stages|文件格式与暂存区（stage）]], [[domains/snowflake/map/ingestion.unload-export|数据卸载（COPY INTO location）]]

## Readings
- [[snowflak-data-loading-overview|数据加载总览:内部/外部 stage 与批量 COPY INTO]]

## Cards (5)
1. [[copy-into-load-metadata-dedupe]]
2. [[copy-into-no-dml-error-logging]]
3. [[copy-into-parallel-across-files]]
4. [[copy-into-simple-transformations]]
5. [[copy-into-user-warehouse-single-txn]]
%% trellis:end %%

## Notes
