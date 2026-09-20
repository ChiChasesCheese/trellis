---
nodes: [problems.commerce.hotel-reservation]
url: https://medium.com/airbnb-engineering/avoiding-double-payments-in-a-distributed-payments-system-2981f6b070bb
tags: [engineering-blog]
---
# Avoiding Double Payments in a Distributed Payments System

值得读：Airbnb 自己的支付平台团队描述了他们的幂等框架 Orpheus——区分请求级（随机键，防网
络重试产生的重复调用）和实体级（确定性键，防同一实体被重复操作，如"同一笔支付只能被退款一
次"）两种幂等键，以及用数据库行锁对幂等键"发放租约"防止并发执行。本题「深入探讨」第 5 节
和 [[solution-ticket-booking]] 的支付编排结论都以此为依据；本篇比多数题解文章更具体的地
方是它给出了真实的生产结果（支付量翻倍的同时一致性做到五个九），而不是抽象地说"用幂等
键"。

%% trellis:begin %%
## Source
[Open the original ↗](https://medium.com/airbnb-engineering/avoiding-double-payments-in-a-distributed-payments-system-2981f6b070bb)
%% trellis:end %%
