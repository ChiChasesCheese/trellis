---
nodes: [problems.social.social-graph-search]
url: https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/social_graph/README.md
---
# system-design-primer — Design Facebook's Friend Search

值得读：MIT 协议的开源社区仓库（CC-BY 授权的解答文档），给出了按 `PersonServer` 分片、
`LookupService` 做用户到分片映射、双向 BFS 找最短路径的基础框架，以及"按地理位置分片，
因为朋友通常住得近"的直觉。本题解没有采用按地理位置分片，而是论证了图分区在数十亿边规模
下的维护代价（NP 难 + 持续腐化）超过它节省的查询成本，选择了更简单的按用户哈希分片。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/social_graph/README.md)

## Archived copy
![[src-donnemartin-social-graph-search-clip]]
%% trellis:end %%
