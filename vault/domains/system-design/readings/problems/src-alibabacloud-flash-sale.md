---
nodes: [problems.commerce.flash-sale]
url: https://www.alibabacloud.com/blog/system-stability-assurance-for-large-scale-flash-sales_596968
tags: [engineering-blog]
---
# System Stability Assurance for Large Scale Flash Sales

值得读：阿里云工程团队自己公开的秒杀技术方案——用商品 ID 做 Redis 键、可用库存做值，
Lua 脚本的事务特性实现"读取剩余库存后扣减"；文中还给出了天猫双十一开场 26 秒峰值每秒 58.3
万笔交易（2009 年首届的 1,457 倍）的真实数字，以及用 AHAS 对热点商品单独限流排队的做法。
本题「深入探讨」第 2 节的核心扣减方案和「瓶颈、故障与演进」100 倍演进一节的真实数字均以此
为依据；本文比它多走一步的地方，是补上了 Redis 作为库存判定真相来源时的持久化风险和对账
兜底，原文没有展开这一层。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.alibabacloud.com/blog/system-stability-assurance-for-large-scale-flash-sales_596968)

## Archived copy
![[src-alibabacloud-flash-sale-clip]]
%% trellis:end %%
