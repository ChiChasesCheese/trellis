%% trellis:begin %%
# 向量检索：HNSW 与 IVF
*AI 工程里的数据结构与算法*

在百万个向量里找最相近的几个：暴力比较太慢；HNSW 是分层的近邻图（上层稀疏、下层稠密，像跳表），从顶层贪心往下走，用堆维护候选；IVF 先聚类，只查最近的几个桶。

## Cards (4)
1. [[uth-ai-vector-search-1-graph-walk]]
2. [[uth-ai-vector-search-2-ef-heaps]]
3. [[uth-ai-vector-search-3-layers]]
4. [[uth-ai-vector-search-4-ivf]]
%% trellis:end %%

## Notes
