%% trellis:begin %%
# 持久化结果缓存
*缓存层*

当 SQL 文本与底层数据均未改变时，零计算成本地返回此前的结果，有效期最长 24 小时。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/snowflake/map/metadata.foundationdb-role|FoundationDB 作为元数据存储]]

**Unlocks:** [[domains/snowflake/map/cache.result-cache-invalidation|结果缓存失效]], [[domains/snowflake/map/cache.cache-layer-tradeoffs|各缓存层的权衡]]

## Readings
- [[snowflak-result-cache|结果缓存(Result Cache)命中与失效条件]]

## Cards (5)
1. [[result-cache-24h-31d-retention]]
2. [[result-cache-exact-text-match]]
3. [[result-cache-nonreusable-functions]]
4. [[result-cache-result-scan-postprocess]]
5. [[result-cache-zero-compute]]
%% trellis:end %%

## Notes
