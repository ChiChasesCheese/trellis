---
nodes: [problems.search.metrics-monitoring]
url: https://www.vldb.org/pvldb/vol13/p3181-adams.pdf
---
# Monarch: Google's Planet-Scale In-Memory Time Series Database

值得读：Google 官方发表于 VLDB 2020 的第一方论文，披露了 leaf/mixer/root 分层查询架构、
field hash index（FHI）把 zone 级查询扇出减少约 99.5%、root 级减少约 80%，以及
"按用户追踪查询内存占用、超预算取消查询"和"查询线程放入按用户划分的 cgroup 保证公平
CPU 份额"这两条真实的多租户隔离机制，论文还披露了 2019 年内部部署约 2.2TB/秒的原始
写入速率。本题解「深入探讨」第 5 节把论文披露的两个扇出削减百分比套用到本设计自己假设
的 20 zone × 500 leaf 拓扑上，重新计算出约 833 倍的扇出降低——这个具体倍数是本文基于
自己拓扑假设的计算，论文本身没有给出这个数字，因为它描述的是 Google 自己真实但未完全
披露的集群规模；第 7 节的多租户隔离机制直接采纳了论文披露的两条真实机制，没有改动。
