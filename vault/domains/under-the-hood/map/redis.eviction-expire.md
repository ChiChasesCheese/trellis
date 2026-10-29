%% trellis:begin %%
# 近似 LRU / LFU 与过期删除
*Redis*

不维护全局 LRU 链表，而是随机采样几个键、淘汰最久未用的；LFU 用对数计数器加衰减；过期键是惰性删除加定期随机抽查。

**Core** — part of the first pass through this subject.

## Cards (3)
1. [[uth-redis-eviction-expire-1-approx-lru]]
2. [[uth-redis-eviction-expire-2-lfu]]
3. [[uth-redis-eviction-expire-3-expire]]
%% trellis:end %%

## Notes
