---
id: hi-c-lld-coordination-x08-actor-order
node: lld.concurrency.coordination.exam
type: qa
step: 8
---
## Q
**并发协调 · Actor 的消息顺序**｜考点 · 追问

账户 actor B 收到来自 A 的"存 100"和来自 C 的"查余额"。B 收到两条消息的顺序是否确定？怎么保证业务正确？

## A
- **同一发送者到同一接收者：** 有序
- **不同发送者：** 交错顺序不确定，查余额可能在存款之前或之后
- **做法：** 业务上接受这个不确定；需要因果顺序时，让 C 等 A 的确认后再发；或把需要顺序的操作放到同一个 actor 里
- **启示：** 别依赖跨发送者的全局顺序
