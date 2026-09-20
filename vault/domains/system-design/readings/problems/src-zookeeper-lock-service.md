---
nodes: [problems.foundations.lock-service]
url: https://www.usenix.org/legacy/event/atc10/tech/full_papers/Hunt.pdf
tags: [reference]
---
# Hunt, Konar, Junqueira, Reed — ZooKeeper: Wait-free coordination for Internet-scale systems (USENIX ATC 2010)

值得读：一手论文，本题解引用了它的 watch 一次性触发语义、临时+顺序节点的锁配方（只 watch
前驱节点以避免惊群）、以及不同集群规模下的饱和读写吞吐实测表——这张表是本题解"为什么不靠
加投票节点扩容"这一论证的核心证据，直接取自论文而非本题解自行假设。和本题解的分歧在于：
论文把"避免惊群"的写法作为一个更优化的版本单独给出，本题解额外强调了"广播反而是期望行为"
这个反例（共享读锁场景），论文原文提到了这一点但没有展开讨论它和排队写法的适用边界。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.usenix.org/legacy/event/atc10/tech/full_papers/Hunt.pdf)

## Archived copy
![[src-zookeeper-lock-service-clip]]
%% trellis:end %%
