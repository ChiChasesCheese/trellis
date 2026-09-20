---
id: patterns-observer-notification-service
node: patterns.observer
type: qa
step: 6
---
## Q
通知服务的多渠道订阅用 Observer 建模时，subject 通知的方式会带来什么设计后果？

## A
如果同步地按订阅顺序逐个调用（先短信、再邮件、再推送），最慢的渠道会拖慢整个请求；如果一个用户同时订阅了多个渠道，还要决定某个渠道失败要不要重试、要不要为每个渠道单独设超时。生产实践通常让 subject 的"通知"本身只是一次快速的入队操作——把事件丢进各渠道自己的队列，真正的发送在订阅者内部异步完成，subject 不等待发送结果。
