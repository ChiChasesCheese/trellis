---
nodes: [problems.social.tinder]
url: https://medium.com/tinder-engineering/geosharded-recommendations-part-1-sharding-approach-d5d54e0ec77a
---
# Geosharded Recommendations Part 1: Sharding Approach

值得读：Tinder 工程团队自己讲清楚了候选人地理分片的动机——单一 Elasticsearch 索引在
规模增长下遇到高 CPU 利用率和高基础设施成本，改用按地理位置切分索引（geosharding）后
用负载分数（load score）和 Google S2 库的 Hilbert 曲线做均衡分片。比大多数题解文章更
具体的地方是给出了真实的分片数量范围（40–100 个）、S2 cell 层级选择（Level-7/8）和
实测的 20 倍计算容量提升，而不是抽象地说"按地理位置分片"。

%% trellis:begin %%
## Source
[Open the original ↗](https://medium.com/tinder-engineering/geosharded-recommendations-part-1-sharding-approach-d5d54e0ec77a)
%% trellis:end %%
