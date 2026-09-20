---
nodes: [problems.geo.food-delivery]
url: https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff
tags: [no-archive]
---
# Design a Local Delivery Service like Gopuff

值得读：商业刷题站 Hello Interview 对 Gopuff 类问题的深度题解——四个核心实体
（Inventory/Item/DistributionCenter/Order）、按距离和行程时间筛选可服务仓库、把
库存查询和下单都放进同一个共享 Postgres 实例的 ACID 事务里防止超卖。本题解「常见
错误」一节明确指出分歧：它没有区分展示层查询和扣减层写入两种负载特征（本题解「容量
估算」算出两者流量相差 20 倍），本题解把二者拆开处理，只让精确库存扣减这一窄操作
承担强一致开销。

%% trellis:begin %%
## Source
[Open the original ↗](https://www.hellointerview.com/learn/system-design/problem-breakdowns/gopuff)
%% trellis:end %%
