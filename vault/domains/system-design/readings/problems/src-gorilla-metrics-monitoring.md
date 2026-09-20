---
nodes: [problems.search.metrics-monitoring]
url: https://www.vldb.org/pvldb/vol8/p1816-teller.pdf
---
# Gorilla: A Fast, Scalable, In-Memory Time Series Database

值得读：Facebook 官方发表于 VLDB 2015 的第一方论文，披露了 delta-of-delta 时间戳编码
和 XOR 浮点值编码的确切位分配规则、2 小时块大小下平均 1.37 字节/点（12 倍压缩比）的生产
集群实测数字、96% 的时间戳可压缩到单比特、数值 XOR 三种分桶各自的占比与平均位数，以及
"每个数据点写两个独立地理 region、节点故障时读请求自动切到健康 region"的可靠性设计。本
题解「深入探讨」第 2 节直接实现了论文描述的算法并在三种合成场景（空闲指标/稳定计数器/
噪声仪表）上重新计算压缩比，而不是照抄论文的生产集群平均数——因为压缩比强依赖指标本身
的变化模式；第 6 节的告警评估容灾设计把论文"写两个 region、故障读切换"的思路应用到告警
评估子系统本身，原文本身只讨论了写路径和查询路径的可靠性，没有专门讨论告警评估路径。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.vldb.org/pvldb/vol8/p1816-teller.pdf)

## Archived copy
![[src-gorilla-metrics-monitoring-clip]]
%% trellis:end %%
