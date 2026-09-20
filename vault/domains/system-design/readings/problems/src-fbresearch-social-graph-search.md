---
nodes: [problems.social.social-graph-search]
url: https://research.facebook.com/blog/2016/2/three-and-a-half-degrees-of-separation/
---
# Three and a Half Degrees of Separation

值得读：Facebook Research 2016 年的博文，在 15.9 亿用户的真实图上，用基于
Flajolet-Martin 的近似算法（而不是精确的全量最短路径计算）估算出平均分隔度约 4.57 跳。
本题解引用这个方法论作为"即便是离线的全站统计量，业界也不追求精确计算"的证据，支撑本
设计把在线最短路径查询设计成有界深度、近似语义的理由。

%% trellis:begin %%
## Source
[Open the original ↗](https://research.facebook.com/blog/2016/2/three-and-a-half-degrees-of-separation/)
%% trellis:end %%
