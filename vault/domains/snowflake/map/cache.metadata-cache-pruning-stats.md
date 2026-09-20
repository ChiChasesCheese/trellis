%% trellis:begin %%
# 用于剪枝的元数据缓存
*缓存层*

直接缓存最小值/最大值/计数等统计信息本身，使剪枝和简单聚合运算完全无需接触数据文件。

**Requires:** [[domains/snowflake/map/storage.micro-partition-metadata|微分区元数据]]

## Cards (5)
1. [[metadata-cache-always-consistent]]
2. [[metadata-cache-count-without-warehouse]]
3. [[metadata-cache-min-max-answerable]]
4. [[metadata-cache-pruning-before-scan]]
5. [[metadata-cache-where-clause-breaks-shortcut]]
%% trellis:end %%

## Notes
