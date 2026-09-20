---
nodes: [problems.geo.proximity, problems.geo.ride-hailing]
url: https://www.uber.com/en-EG/blog/h3/
---
# H3: Uber's Hexagonal Hierarchical Spatial Index

值得读：Uber 官方工程博客解释了 H3 用 122 个基础单元加 12 个五边形（放在海洋上以减小
拓扑影响）覆盖全球、支持 16 级分辨率（每细一级面积约变为上一级的 1/7）、以及六边形相对
正方形网格"到所有邻居的中心距离一致"这一核心几何性质。与本题解不同的地方在于：proximity
一题里本题解把这个性质接到了"候选集边界查询"和"密度自适应"上，ride-hailing 一题里则
接到了"周边供需密度插值/动态定价为什么需要均匀邻居距离"这个更具体的应用场景，原文只泛泛
提到"优化定价和调度"，没有展开为什么均匀性对这两类计算分别重要。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.uber.com/en-EG/blog/h3/)
%% trellis:end %%
