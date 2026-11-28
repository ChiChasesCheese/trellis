---
id: hi-c-lld-coordination-x07-queue-or-actor
node: lld.concurrency.coordination.exam
type: qa
step: 7
---
## Q
**并发协调 · 队列还是 actor**｜考点 · 必会

选择：(a) 注册后发欢迎邮件；(b) 聊天系统里每个房间有自己的成员列表和消息历史；(c) 每个交易品种有自己的订单簿，必须顺序处理。

## A
| 场景 | 选择 | 理由 |
|---|---|---|
| 欢迎邮件 | 阻塞队列加工人池 | 只是后台处理任务 |
| 聊天房间 | actor | 各房间状态独立，顺序处理消息 |
| 订单簿 | actor | 每个订单簿独占数据，串行处理，无需锁 |

- 面试默认答队列，再说明何时换 actor
