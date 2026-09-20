---
nodes: [problems.foundations.cdn]
url: https://blog.cloudflare.com/instant-purge/
tags: []
---
# Instant Purge: invalidating cached content in under 150ms

值得读：Cloudflare 公开的 purge 传播架构，把全网 purge 的 P50 延迟做到 150 毫秒以
内，是一手数据而不是转述。题解「深入探讨」第 3 节用它证明"秒级以下的全网 purge 传播
在工程上可达"，但为本题自己的设计设定了更保守的 2 秒 P99 目标，因为不假设拥有为 purge
单独优化的专用网络层。

%% trellis:begin %%
## Source
[Open the original ↗](https://blog.cloudflare.com/instant-purge/)

## Archived copy
![[src-cloudflare-purge-cdn-clip]]
%% trellis:end %%
