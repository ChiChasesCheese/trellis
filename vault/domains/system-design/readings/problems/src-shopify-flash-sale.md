---
nodes: [problems.commerce.flash-sale]
url: https://shopify.engineering/surviving-flashes-of-high-write-traffic-using-scriptable-load-balancers-part-i
tags: [engineering-blog]
---
# Surviving Flashes of High-Write Traffic Using Scriptable Load Balancers (Part I & II)

值得读：Shopify 自己 2016 年被 Kylie Cosmetics 一场秒杀打垮所在数据库分片的真实事故复
盘，以及后续演化出的边缘限流+排队页方案——第一版纯随机限流导致排队时间方差极大、体验不公
平，第二版引入 PID 控制器动态调整放行阈值以收窄这个方差。本题「深入探讨」第 1 节的准入控
制组合方案和「面试官会追问什么」参谋级问题里"用反馈控制动态校准放行速率"的思路直接借鉴这
篇文章；本文额外加入了抽签模式作为先到先得之外的选项，是这篇 Shopify 文章没有涉及的部
分。

%% trellis:begin %%
## Source
[Open the original ↗](https://shopify.engineering/surviving-flashes-of-high-write-traffic-using-scriptable-load-balancers-part-i)

## Archived copy
![[src-shopify-flash-sale-clip]]
%% trellis:end %%
