---
id: async-queue-vs-pubsub
node: async.queues
type: qa
---
## Q
When do you choose a work queue (competing consumers) over pub/sub fan-out?

## A
- **Work queue**: each message is a *task* that exactly one consumer should perform (send email, resize image). Consumers compete; adding consumers increases throughput.
- **Pub/sub**: each message is a *fact* that multiple independent subscribers each need (order-placed → billing, analytics, notifications). Every subscriber group gets its own copy.
- Rule of thumb: one owner of the side effect → queue; many downstream reactions → pub/sub.

## Q zh
何时选择工作队列（竞争 consumer）而不是 pub/sub 扇出？

## A zh
- **工作队列**：每条消息是一个*任务*，正好一个 consumer 应该执行（发邮件、调整图像大小）。Consumer 竞争；添加 consumer 增加吞吐量。
- **Pub/sub**：每条消息是一个*事实*，多个独立订阅者各自需要（order-placed → billing、analytics、notifications）。每个订阅者 group 获得自己的副本。
- 经验法则：副作用的单一所有者 → 队列；多个下游反应 → pub/sub。
