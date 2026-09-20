---
nodes: [problems.commerce.hotel-reservation]
url: https://medium.com/expedia-group-tech/choosing-the-right-candidates-for-lodging-ranking-d0841bf40c0e
tags: [engineering-blog]
---
# Choosing the Right Candidates for Lodging Ranking

值得读：Expedia 自己的工程团队点出了"给定搜索查询，对每个房源按房型取可用性和价格"这一步
计算上特别昂贵、会产生组合爆炸，并给出了"纽约、洛杉矶、奥兰多等中等目的地单地就有一万多个
房源"这个一手数字。比大多数题解文章更具体的地方是它明确了两阶段（先收窄候选、再对小候选集
做昂贵定价）不是理论上的优化建议，而是他们真实生产系统的做法；本题据此设计了搜索索引与权
威可用性查询这两条物理上独立的路径，比文章本身多走一步的地方是把这个两阶段落到了两套不同
的存储技术上。

%% trellis:begin %%
## Source
[Open the original ↗](https://medium.com/expedia-group-tech/choosing-the-right-candidates-for-lodging-ranking-d0841bf40c0e)
%% trellis:end %%
