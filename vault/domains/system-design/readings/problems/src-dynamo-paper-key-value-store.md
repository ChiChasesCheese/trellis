---
nodes: [problems.foundations.key-value-store]
url: https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf
tags: [paper]
---
# Dynamo: Amazon's Highly Available Key-value Store
值得读：这是本题解的核心一手来源——SOSP 2007 论文原文，第一次系统性地把一致性哈希、
sloppy quorum、hinted handoff、vector clock 和 Merkle 树反熵组合成一套生产系统,并公开
了 N=3/R=2/W=2 的生产配置和"峰值 500 请求/秒下 99.9% 请求在 300ms 内完成"的真实 SLA。
本题解与论文的不同：论文本身不给出某个具体业务规模下需要多少物理/虚拟节点这类容量估算，
本题解把论文描述的机制套进一个假设的 3 亿月活场景，推导出约 167 台物理节点、约 2,672
个虚拟节点这类具体数字，供读者理解"这些机制在什么规模下真正开始起作用"。
