---
id: amz-parking-fees-concurrency-two-exits-one-ticket
node: amazon.amz-parking-fees
type: qa
step: 8
tags: [grown]
---
## Q
在 Amazon 停车场计费设计里，两个出口同时扫同一张票，会出什么问题？怎么保证只收一次钱？

## A
问题是「查票存在」与「删除票」被拆成两步：两个线程都查到票在，各自算费并放行。GIL 只保证单条字节码原子，不保证这两步连在一起。做法：`FeeDesk` 用一把锁，在锁内用 `dict.pop` 一次性取走票，取不到的抛 `UnknownTicketError`；计价本身是纯计算，放在锁外。16 个线程同时出场同一张票，恰好 1 个拿到收据，15 个收到异常；已结算的票不再保留，所以票表不会无限增长。
