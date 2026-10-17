---
id: amz-emergency-pubsub-failure-boundary-in-subscription
node: amazon.amz-emergency-pubsub
type: qa
step: 5
tags: [grown]
---
## Q
在应急发布订阅里，「一个订阅者抛异常不能拖累其他人」这条保证应该放在哪一层实现？有哪些选择？

## A
三个位置：(1) `publish` 的整个循环外包一层 try：出错者之后的订阅者全收不到；(2) 要求订阅者自己不抛：一个 bug 就破坏全局；(3) `Subscription.deliver` 内部只对 `Exception` 做 try/except，换成一条 `DeadLetter` 返回。选 (3)：边界只有一处，同步和异步共用，`KeyboardInterrupt` 这类 `BaseException` 仍然放行。
