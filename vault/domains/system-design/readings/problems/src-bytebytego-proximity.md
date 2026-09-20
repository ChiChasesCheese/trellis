---
nodes: [problems.geo.proximity]
url: https://bytebytego.com/guides/proximity-service
tags: [no-archive]
---
# Proximity Service

值得读：ByteByteGo 的邻近服务设计指南给出了业务服务（Business Service）和基于位置的
服务（Location-Based Service）两个组件拆分的基本思路，以及 geohash 编码后可以直接用
`LIKE '01%'` 这类前缀查询命中索引的写法。与本题解不同的地方在于：本题解把"网格密度不均"
这一局限性用具体数字量化（同精度网格在城市中心和郊区的商户密度可以相差几十到上百倍），
并给出了 quadtree 作为密度自适应替代方案的完整索引项开销对比，原文只停留在定性指出问题。

%% trellis:begin %%
## Source
[Open the original ↗](https://bytebytego.com/guides/proximity-service)
%% trellis:end %%
