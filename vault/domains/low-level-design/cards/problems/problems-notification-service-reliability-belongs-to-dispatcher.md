---
id: problems-notification-service-reliability-belongs-to-dispatcher
node: problems.components.notification-service
type: qa
step: 1
tags: [grown]
---
## Q
设计通知服务（多渠道发送 email / SMS / push）时，重试、限流、去重、优先级这些可靠性逻辑该写在哪？装饰器栈（`RetryingChannel(RateLimitedChannel(EmailChannel()))`）和派发器管道各有什么代价？

## A
写在**派发器**里一份。一句可以背的判据：**渠道之间共享的东西归派发器，渠道之间不同的东西归渠道**；渠道最后只剩一个名字和一个会失败的 `send`。

装饰器栈很漂亮，但有两处代价：（1）**每个渠道都要各自包一遍**，四个渠道四条装饰链，忘了给新渠道包重试，它就悄悄没有重试；（2）致命的一处——**跨渠道的策略没有地方站**。『这个用户一小时最多收 5 条，无论哪个渠道』和『验证码要排在营销前面』都不属于任何单个渠道。优先级尤其尴尬：装饰器是同步调用链，而优先级只有在**排队**时才有意义。

装饰器不是全错：某个渠道自己需要一层包装（短信网关的本地熔断器）时，在那一个 provider 外面包一层仍然对。
