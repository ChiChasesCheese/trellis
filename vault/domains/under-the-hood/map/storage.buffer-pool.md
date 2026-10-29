%% trellis:begin %%
# 缓冲池替换：中点 LRU 与时钟扫描
*数据库与搜索引擎*

InnoDB 把 LRU 链表分成新老两段防止全表扫描冲掉热页；PostgreSQL 用时钟扫描（clock sweep）近似 LRU。

## Cards (3)
1. [[uth-storage-buffer-pool-1-midpoint-lru]]
2. [[uth-storage-buffer-pool-2-clock-sweep]]
3. [[uth-storage-buffer-pool-3-ring-buffer]]
%% trellis:end %%

## Notes
