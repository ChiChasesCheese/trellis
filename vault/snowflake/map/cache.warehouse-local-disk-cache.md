%% trellis:begin %%
# 仓库本地 SSD 缓存
*缓存层*

每个节点上缓存近期扫描过的微分区的本地磁盘缓存，仓库一旦挂起就会丢失该缓存。

**Requires:** [[warehouse.sizing-t-shirt|仓库规格（T 恤尺码式）]]

**Unlocks:** [[cache.cache-layer-tradeoffs|各缓存层的权衡]]

## Readings
- [[snowflak-warehouse-best-practices|仓库调优:扩容(up)还是扩出(out)、本地磁盘缓存]]

## Cards (5)
- [[warehouse-cache-dropped-on-downsize]]
- [[warehouse-cache-dropped-on-suspend]]
- [[warehouse-cache-scales-with-size]]
- [[warehouse-cache-suspend-vs-keep-running-tradeoff]]
- [[warehouse-cache-warms-automatically]]
%% trellis:end %%

## Notes
