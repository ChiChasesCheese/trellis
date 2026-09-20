---
nodes: [problems.commerce.digital-wallet]
url: https://research.google.com/archive/spanner-osdi2012.pdf
tags: [paper]
---
# Spanner: Google's Globally-Distributed Database (OSDI 2012)

值得读：Spanner 论文披露了跨 Paxos 复制组的分布式事务由各组 leader 协同完成两阶段
提交、协调者状态本身也持久化在一个 Paxos 组里这一真实架构，以及事务跨越的副本组物理
距离越远、协调延迟越高这一现实约束。与本题解不同的地方在于：本题解把"协调延迟随物理
距离增长"这一点用作 100 倍演进部分"是否需要按区域给协调者分区、给同区域转账保留快
路径"这一产品权衡的论据，原文本身是数据库系统论文，不涉及这类产品层面的路径分级设计。

%% trellis:begin %%
## Source
[Open the original ↗](https://research.google.com/archive/spanner-osdi2012.pdf)

## Archived copy
![[src-spanner-digital-wallet-clip]]
%% trellis:end %%
