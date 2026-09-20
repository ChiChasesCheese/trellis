---
nodes: [problems.geo.proximity, problems.geo.ride-hailing]
url: https://s2geometry.io/
---
# S2 Geometry Library

值得读：Google S2 官方文档说明了它把地球投影到外接立方体六个面、用希尔伯特曲线
（Hilbert curve）编号、支持 30 级分辨率、第 12 级平均单元面积 3.31–6.38 平方公里的
核心事实。与本题解不同的地方在于：proximity 一题用它和 geohash 的 Z 字形曲线
（Z-order curve）做局部性对比，ride-hailing 一题则引用同一个第 12 级数字作为 Uber
调度系统真实使用的分片粒度，两题共享这份原始几何事实但各自接到不同的设计结论上。

%% trellis:begin %%
## Source
[Open the original ↗](https://s2geometry.io/)
%% trellis:end %%
