---
nodes: [problems.commerce.e-commerce]
url: https://aws.amazon.com/builders-library/caching-challenges-and-strategies/
tags: [engineering-blog, no-archive]
---
# Caching challenges and strategies

值得读：AWS Builders' Library 官方文章，提出"软 TTL 触发刷新、硬 TTL 兜底可用性"
的双 TTL 思路，以及"命中率不好的数据不值得缓存"的判断标准（每次请求都产生不同结果
的查询，缓存收益趋近于零）。本题解「深入探讨」第 5 节的商品页分层新鲜度策略（静态
字段长 TTL、价格/库存字段短 TTL + 写穿透）直接采用了这个双 TTL 框架，并补充了这篇
文章没有覆盖的问题：结账那一刻的强一致权威判定如何和这层"允许陈旧"的缓存共存而不
互相矛盾。

%% trellis:begin %%
## Source
[Open the original ↗](https://aws.amazon.com/builders-library/caching-challenges-and-strategies/)

## Archived copy
![[aws-caching-challenges-clip]]
%% trellis:end %%
