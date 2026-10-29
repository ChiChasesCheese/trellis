%% trellis:begin %%
# Caffeine 缓存：哈希表 + 访问队列 + 频率草图 + 时间轮
*数据结构组合：开源框架里的类设计*

比 LRU 命中率更高的 W-TinyLFU：一个并发哈希表存数据，几条按访问顺序排的双向队列决定淘汰谁，一个计数草图估算访问频率决定新数据能否挤进来，按条目设置的过期时间用时间轮管理，读写先记进缓冲区再批量处理。

**Core** — part of the first pass through this subject.

## Cards (5)
1. [[uth-compose-caffeine-1-needs]]
2. [[uth-compose-caffeine-2-structures]]
3. [[uth-compose-caffeine-3-invariants-code]]
4. [[uth-compose-caffeine-4-concurrency]]
5. [[uth-compose-caffeine-5-ttl-lru]]
%% trellis:end %%

## Notes
