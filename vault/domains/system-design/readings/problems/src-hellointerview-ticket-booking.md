---
nodes: [problems.commerce.ticket-booking]
url: https://www.hellointerview.com/learn/system-design/problem-breakdowns/ticketmaster
tags: [no-archive]
---
# Design a Ticket Booking Site Like Ticketmaster

值得读：Hello Interview 对这道题给出了最完整的免费题解框架——从需求、数据模型、API 一路
展开到三个深入探讨（防止超卖的锁策略演进、10M 并发读的扩展、虚拟排队厅），并按 mid/senior/
staff 分层写出面试官对每个深度的期望。它把"座位占用锁"从 `SELECT FOR UPDATE` 一路演化到
"数据库状态字段 + Redis 分布式锁"的推荐方案，本文的深入探讨部分沿用了同样的演化框架，但在
最终选择上不同：本文认为 Redis 锁与数据库状态字段是两套需要维护一致性的真相来源，更倾向
只用数据库原生条件更新作为唯一真相来源（详见本题题解「深入探讨」第 1 节）。
