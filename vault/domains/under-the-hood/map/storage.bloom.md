%% trellis:begin %%
# 布隆过滤器：LSM 的读路径
*数据库与搜索引擎*

每个 SST 文件一个布隆过滤器，查不存在的键时跳过整个文件；每个键约 10 位时误判率约 1%。

## Cards (3)
1. [[uth-storage-bloom-1-skip-file]]
2. [[uth-storage-bloom-2-cache-line]]
3. [[uth-storage-bloom-3-bits-vs-fp]]
%% trellis:end %%

## Notes
