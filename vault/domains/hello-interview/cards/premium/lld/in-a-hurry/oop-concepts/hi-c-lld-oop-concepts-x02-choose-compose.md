---
id: hi-c-lld-oop-concepts-x02-choose-compose
node: lld.in-a-hurry.oop-concepts.exam
type: qa
step: 2
---
## Q
**面向对象概念 · 重试逻辑放继承还是组合**｜考点 · 必会

邮件、短信、推送三种通知渠道都需要"失败重试三次"。用 `Notifier` 基类写重试，还是把重试做成独立组件？

## A
- **基类方案：** 重试逻辑共享，简单；但每个子类要在重试流程的固定位置插入自己的发送逻辑，基类一改所有渠道都受影响
- **组合方案：** `Channel` 接口只管发送；`RetryingChannel(channel, attempts)` 包住任意渠道
- **选组合：** 重试是正交的横切行为，将来想给某渠道加限流、日志也可叠加
- **继承够用的情形：** 逻辑稳定、全是"一种通知"且不会混搭，也可接受，要说明理由
