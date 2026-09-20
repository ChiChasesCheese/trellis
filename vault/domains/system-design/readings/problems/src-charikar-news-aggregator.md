---
nodes: [problems.search.news-aggregator]
url: https://dl.acm.org/doi/10.1145/509907.509965
---
# Similarity Estimation Techniques from Rounding Algorithms

值得读：Moses Charikar 在 STOC 2002 发表的第一方论文（ACM 官方记录），提出了基于随机
超平面（random hyperplane）舍入的哈希方案——这正是 SimHash 的理论基础：两个特征向量的
随机超平面哈希结果一致的概率，直接和它们的夹角/余弦相似度关联。本题解「深入探讨」第 2
节采用了这个技术构造单一定长指纹的做法，作为和 Broder 式多维 MinHash 签名相对的另一个
方案，并在本设计自己的语料规模上重新计算了内存占用对比；原文是纯理论构造论文，不涉及
新闻聚合或网页去重的具体应用场景，应用层的参数和场景都是本题解自己补上的。
