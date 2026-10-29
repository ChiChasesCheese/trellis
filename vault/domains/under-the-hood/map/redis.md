%% trellis:begin %%
# Redis

每种数据类型底下的编码、渐进式 rehash、跳表、近似 LRU、过期采样、HyperLogLog、单线程事件循环与 fork 持久化。

## Topics
- [[domains/under-the-hood/map/redis.sds-dict|SDS 与 dict：渐进式 rehash]]
- [[domains/under-the-hood/map/redis.zset|ZSET：跳表 + 哈希表]]
- [[domains/under-the-hood/map/redis.compact-encodings|listpack、quicklist、intset：小数据的紧凑编码]]
- [[domains/under-the-hood/map/redis.eviction-expire|近似 LRU / LFU 与过期删除]]
- [[domains/under-the-hood/map/redis.hyperloglog-bitmap|HyperLogLog 与位图]]
- [[domains/under-the-hood/map/redis.event-loop-persistence|单线程事件循环与 fork 持久化]]
- [[domains/under-the-hood/map/redis.streams-geo|Streams 与 GEO]]
%% trellis:end %%

## Notes
