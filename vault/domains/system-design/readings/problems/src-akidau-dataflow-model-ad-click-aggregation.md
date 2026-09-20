---
nodes: [problems.search.ad-click-aggregation]
url: https://www.vldb.org/pvldb/vol8/p1792-Akidau.pdf
tags: []
---
# The Dataflow Model: A Practical Approach to Balancing Correctness, Latency, and Cost in Massive-Scale, Unbounded, Out-of-Order Data Processing

值得读：Google 的 Dataflow 论文（VLDB 2015），本题「深入探讨」第 2、3 节关于水位线是
"系统认为数据大概率到齐了"的启发式估计而非正确性保证、以及 Accumulating & Retracting
触发模式（先发撤回再发新值，供下游二级聚合正确处理）的论证直接来自这篇论文。论文开篇的
动机案例本身就是"给广告计费"，和本题场景高度一致；论文覆盖的窗口合并策略和触发器组合比
本题用到的更完整，本题没有展开会话窗口合并的细节。
