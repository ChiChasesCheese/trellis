---
id: patterns-observer-partial-failure
node: patterns.observer
type: qa
step: 4
---
## Q
某个订阅者的回调抛出异常，为什么不该让它中断其余订阅者的通知？

## A
Observer 的订阅者之间本该互不相关——短信渠道发送失败，不该连累邮件渠道收不到通知。notify 循环里要为每个订阅者单独 `try/except`，记录日志或收集异常列表，遍历完再统一处理，而不是让第一个异常直接向上传播、打断整个通知过程。
