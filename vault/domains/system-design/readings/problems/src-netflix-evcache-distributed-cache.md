---
nodes: [problems.foundations.distributed-cache]
url: https://netflixtechblog.com/caching-for-a-global-netflix-7bcc457012f1
tags: [engineering-blog]
---
# Caching for a Global Netflix
值得读：Netflix 官方工程博客一手来源，披露了 EVCache（Netflix 基于 Memcached 构建的
分布式缓存）跨多个 AWS 区域复制的架构，让任意区域都能以内存级延迟就近服务任意用户。
本题解「深入探讨」第 4 节"冷启动时从对等区域预热而不是从零开始扛数据库回源风暴"这个
方案，直接借鉴了这篇文章披露的"新区域从已经暖机的区域复制内容"这个真实机制；本题解
和它的分歧在于：这篇文章更大篇幅讨论的是跨区域路由和流量切换本身，本题解只取用了它
在冷启动预热这一点上的机制，未涉及全球流量调度的具体拓扑。

%% trellis:begin %%
## Source
[Open the original ↗](https://netflixtechblog.com/caching-for-a-global-netflix-7bcc457012f1)
%% trellis:end %%
