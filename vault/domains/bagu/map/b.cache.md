%% trellis:begin %%
# 缓存问题
*B 其余知识点*

缓存与数据库一致性、穿透击穿雪崩、热 key 大 key、多级缓存、LRU。

## Topics
- [[domains/bagu/map/b.cache.bloom-filter|布隆过滤器原理与误判（Bloom Filter）]]
- [[domains/bagu/map/b.cache.breakdown|缓存击穿（Hotspot Invalid）：互斥重建、逻辑过期、singleflight]]
- [[domains/bagu/map/b.cache.avalanche|缓存雪崩（Cache Avalanche）]]
- [[domains/bagu/map/b.cache.big-key|大 key 的危害与处理（Big Key）]]
- [[domains/bagu/map/b.cache.multilevel|多级缓存设计与冷启动（Local + Redis, Cold Start）]]
- [[domains/bagu/map/b.cache.hit-rate|缓存命中率与容量估算]]
- [[domains/bagu/map/b.cache.lru|LRU 缓存的实现（LRU Cache, LinkedHashMap, TTL, LFU）]]
%% trellis:end %%

## Notes
