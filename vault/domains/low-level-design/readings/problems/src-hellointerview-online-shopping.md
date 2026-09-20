---
nodes: [problems.marketplaces.online-shopping]
url: https://www.hellointerview.com/learn/low-level-design/problem-breakdowns/inventory-management
tags: [no-archive]
---
# Hello Interview — Inventory Management

值得读：把库存从"在线购物"这道大题里单独拎出来当一道题讲，对"现货（on hand）／预留
（reserved）／可用（available）"这三个量的区分讲得很清楚，本题解的不变式
`可用量 == 现货 - 未过期预留之和` 和它是同一个口径；它也把"什么时候扣库存"当作这类题的
中心问题来处理。
不同之处：它更偏服务端视角（分布式锁、数据库事务、乐观并发控制），本题解是单进程内存模型，
用注入的时钟 + 一把可重入锁把同一条不变式守住，并把分布式那部分的取舍放到"扩展与追问"里讲；
它也不涉及订单状态机与跨参与方的补偿。
