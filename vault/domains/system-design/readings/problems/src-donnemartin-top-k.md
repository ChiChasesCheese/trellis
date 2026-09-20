---
nodes: [problems.search.top-k]
url: https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/sales_rank/README.md
tags: []
---
# Design Amazon's sales rank by category feature

值得读：同一类"类目内 Top 排行"问题的批处理对照解法——用 MapReduce 按小时聚合，写入 SQL
索引表，不追近实时新鲜度。和本题的近实时、误差可控的流式方案形成清晰对比，说明"新鲜度
要求"才是决定要不要上 sketch 结构的关键变量，而不是数据量本身。

%% trellis:begin %%
## Source
[Open the original ↗](https://github.com/donnemartin/system-design-primer/blob/master/solutions/system_design/sales_rank/README.md)
%% trellis:end %%
