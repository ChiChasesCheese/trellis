---
id: hi-c-lld-coordination-n09-actor-vs-queue
node: lld.concurrency.coordination.notes
type: qa
step: 9
---
## Q
**并发协调 · Actor 与阻塞队列：何时选哪个**｜摘要 · 必会

Actor 和阻塞队列加工人池，思路上差在哪？什么时候选 actor？

## A
- **队列加工人池：** 想的是共享数据和同步，多个工人处理的任务可能碰同一份数据，仍需要锁
- **Actor：** 想的是消息和所有权，每个 actor 独占自己的数据；邮件客户端归 `EmailActor`，别人只能 `send`
- **选 actor：** 许多独立、各有状态的实体偶尔通信（聊天会话、游戏房间、订单簿）；还便于分布到多台机器
- **选队列：** 只是"后台处理这些任务"，更简单直接
- **代价：** 消息类型、生命周期、投递保证这些概念开销
