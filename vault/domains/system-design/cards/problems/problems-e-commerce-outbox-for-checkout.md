---
id: problems-e-commerce-outbox-for-checkout
node: problems.commerce.e-commerce
type: qa
step: 7
tags: [grown]
---
## Q
In an e-commerce checkout, why does the Checkout Orchestrator write the Order row and the saga-kickoff event in the same local transaction instead of writing the order and then publishing the event afterward?

## A
Writing the order and publishing separately is the dual-write problem: a crash between the two steps leaves an order with no event to drive it (inventory silently stays reserved and payment never gets triggered) — an order that appears created but never gets acted on. Writing both the Order row and an outbox event row in one local transaction (the transactional outbox pattern) guarantees they are atomic: either both exist or neither does. A relay then delivers the outbox row to the queue at-least-once, and downstream workers dedupe by the event id so a redelivered event can't trigger payment or fulfillment twice.

## Q zh
在电商结账中，为什么 Checkout Orchestrator 要在同一个本地事务里写 Order 行和触发 saga 的事件，而不是先写订单再单独发布事件？

## A zh
分开写订单和发布事件是典型的双写问题：两步之间崩溃会留下一个没有事件驱动它的订单（库存悄悄保持预留状态，支付永远不会被触发）——一个看起来已创建却永远不会被处理的订单。在同一个本地事务里写 Order 行和一条 outbox 事件行（事务型 outbox 模式）保证两者原子：要么都存在要么都不存在。之后 relay 以至少一次的方式把 outbox 行投递到队列，下游 worker 按事件 id 去重，这样重复投递的事件不会把支付或履约触发两次。
