---
nodes: [problems.foundations.url-shortener]
url: https://algomaster.io/learn/system-design-interviews/design-url-shortener
tags: [no-archive]
---
# Design URL Shortener

值得读：给出 Snowflake 风格的 64 位分布式 ID（时间戳 + worker id + 序列号）作为计数器方案的替代实现，并详细讨论了乐观并发写（DynamoDB 条件写）处理自定义别名竞态。本题解认为 Snowflake 式方案在本题这种低写入 QPS 场景下引入的时钟同步依赖是不必要的开销，故未采用，但保留了它对条件写解决 TOCTOU 竞态的论证。

%% trellis:begin %%
## Source
[Open the original ↗](https://algomaster.io/learn/system-design-interviews/design-url-shortener)
%% trellis:end %%
