---
nodes: [problems.geo.proximity]
url: https://en.wikipedia.org/wiki/Geohash
---
# Geohash

值得读：Wikipedia 的 Geohash 条目给出了精确的编码算法（纬度/经度二进制位交替编织、
Base32 字符表）和逐字符长度对应的误差半径表（长度 6 约 ±610 米，长度 8 约 ±19 米）。
与本题解不同的地方在于：本题解把这份精度表换算成了"同精度网格在城市中心和郊区的商户
密度可以相差几十到上百倍"这一具体的密度失衡后果，并用它来论证为什么这道题选 quadtree
而不是纯 geohash 作为主索引，原文只描述编码机制本身。

%% trellis:begin %%
## Source
[Open the original ↗](https://en.wikipedia.org/wiki/Geohash)

## Archived copy
![[src-wikipedia-geohash-clip]]
%% trellis:end %%
