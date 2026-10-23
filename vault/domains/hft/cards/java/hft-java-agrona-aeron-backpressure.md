---
id: hft-java-agrona-aeron-backpressure
node: java.agrona-aeron
type: qa
step: 5
---
## Q
使用 Aeron 发消息时，如果接收方跟不上或连接断开，会发生什么？调用方应该怎么办？

## A
`Publication.offer()` 不会阻塞，也不抛异常，而是返回一个**负数状态码**：`NOT_CONNECTED`（-1，没有订阅者）、`BACK_PRESSURED`（-2，接收方跟不上，流控窗口满了）、`ADMIN_ACTION`（-3，正在做内部管理动作）、`CLOSED`（-4）、`MAX_POSITION_EXCEEDED`（-5，流达到上限）。成功则返回新的位置（正数）。

调用方必须自己处理：对 `BACK_PRESSURED` 和 `ADMIN_ACTION`，通常用 `IdleStrategy` 短暂自旋后重试；对 `NOT_CONNECTED` 要决定等待还是上报告警；在行情分发这类场景，也可以选择丢弃过期的数据。这是一种明确的**背压**（back pressure）设计：让慢的一方显式暴露出来，而不是悄悄占满队列、内存暴涨。
