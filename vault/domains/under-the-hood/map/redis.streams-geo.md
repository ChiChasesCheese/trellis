%% trellis:begin %%
# Streams 与 GEO
*Redis*

Streams 用基数树（rax）按 ID 索引 listpack；GEO 把经纬度编码成 geohash 存进 ZSET，附近查询就是有序集合的范围查询。

**Core** — part of the first pass through this subject.

## Cards (3)
1. [[uth-redis-streams-geo-1-stream-rax]]
2. [[uth-redis-streams-geo-2-delta]]
3. [[uth-redis-streams-geo-3-geo]]
%% trellis:end %%

## Notes
