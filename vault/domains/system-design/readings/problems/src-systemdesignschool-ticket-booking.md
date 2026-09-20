---
nodes: [problems.commerce.ticket-booking]
url: https://systemdesignschool.io/problems/ticketmaster/solution
tags: [no-archive]
---
# Ticketmaster (Ticket Booking) System Design

值得读：System Design School 的题解把"强一致性只用在占座这一个写点、浏览路径完全弱一致"
讲得比大多数免费题解都清楚，并给出了一组具体的容量数字（5 万座位、100 万买家、17K
holds/秒、3.3M 浏览读/秒），比 Hello Interview 更强调座位表是唯一真相来源、缓存永远只是
派生视图。本文容量估算一节独立推导了自己的一组数字，量级与它一致但假设不同（本文用 20:1
的平均竞争比和分层的排队放行速率，而不是直接假设峰值全量涌向数据库），可以互相印证。
