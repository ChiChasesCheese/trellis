---
nodes: [problems.foundations.url-shortener]
url: https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly
tags: [no-archive]
---
# Bitly - System Design

值得读：按面试等级（mid/senior/staff）拆出不同深度的期望，并把"计数器批量领取减少 Redis 调用"讲得很清楚。它把 Redis 计数器本身当作短码生成的唯一来源；本题解不同之处在于把计数器协调抽象成独立的 KGS 服务，强调该服务离线时只影响创建、不影响重定向这条隔离性质，这一点原文没有单独展开。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.hellointerview.com/learn/system-design/problem-breakdowns/bitly)
%% trellis:end %%
