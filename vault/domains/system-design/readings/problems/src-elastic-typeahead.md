---
nodes: [problems.search.typeahead]
url: https://www.elastic.co/guide/en/elasticsearch/reference/current/near-real-time.html
---
# Near real-time search

值得读：Elasticsearch 官方文档说明补全建议器（completion suggester）把候选结构整体
保持在堆内存里以换取查询速度、构建代价高，并通过 refresh 机制近实时对新写入可见——是
"预计算结构 vs 实时可更新"这个权衡最权威的一手说明。本题解在「深入探讨」第 1 节引用了
它"in-memory、构建代价高"这一权衡，但把具体的数据结构对比（trie 现算 vs 预计算 top-K
vs FST）和构建/更新代价的量化论证做成了本题解自己的分析，不停留在原文的一般性描述。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.elastic.co/guide/en/elasticsearch/reference/current/near-real-time.html)
%% trellis:end %%
