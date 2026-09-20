---
nodes: [problems.foundations.cdn]
url: https://www.fastly.com/blog/let-the-edge-work-for-you-how-shielding-improves-performance
tags: []
---
# Let the edge work for you: How shielding improves performance

值得读：Fastly 官方博客，讲清楚 shield POP 如何把多个边缘节点的未命中流量汇聚到一
个节点再回源，并直接给出"平均而言，配置了 shielding 的客户能把高达 99% 的请求挡在
边缘、不触达源站"这句话。题解「深入探讨」第 2 节的源站保护倍数计算（5x/20x）建立在
这篇文章描述的同一机制上，只是用了本题自己假设的边缘/屏蔽层数量而不是 Fastly 的真实
拓扑数字。
