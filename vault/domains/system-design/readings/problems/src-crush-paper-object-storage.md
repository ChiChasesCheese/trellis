---
nodes: [problems.foundations.object-storage]
url: https://ceph.com/assets/pdfs/weil-crush-sc06.pdf
tags: []
---
# CRUSH: Controlled, Scalable, Decentralized Placement of Replicated Data

值得读：SC 2006 论文，第一手描述了 Ceph 采用的放置算法——不查中心化的位置表，
而是对一个描述集群拓扑的层级化 cluster map 做确定性伪随机哈希，客户端和存储节点
都能独立算出同一个放置结果，拓扑变化时只有被改变的那一支需要重新映射。题解「深入
探讨」第 2 节采用这个思路作为数据放置方案，但没有实现论文里针对不同故障域权重的
完整规则语言（rule language），是一个简化版本。
