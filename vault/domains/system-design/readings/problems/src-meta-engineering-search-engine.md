---
nodes: [problems.search.search-engine]
url: https://engineering.fb.com/2013/03/14/core-infra/under-the-hood-indexing-and-ranking-in-graph-search/
---
# Under the Hood: Indexing and ranking in Graph Search

值得读：Meta 工程博客披露了 Unicorn 索引框架的真实架构——索引按不同实体类型切成多个
"垂直（vertical）"，每个垂直内部再分片，由聚合器逐层合并各分片和各垂直的结果，而不是
单层扁平的 scatter-gather。本题解在「瓶颈、故障与演进」的 100 倍演进部分采用了同一个
分级聚合思路，用来解决扇出宽度随分片数持续增长而自身成为瓶颈的问题；原文没有给出量化的
分片数或延迟数字，本题解自己按容量估算重新算出了分片数量级和长尾概率，与原文的差异在
这一层的具体数字。
