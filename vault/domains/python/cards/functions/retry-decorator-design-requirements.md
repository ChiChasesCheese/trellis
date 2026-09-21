---
id: retry-decorator-design-requirements
node: functions.decorator-patterns
type: qa
tags: [grown]
---
## Q
设计一个通用的 retry 装饰器，除了「重试次数」之外，还必须能配置哪两件事，才不会把不该重试的错误也吞掉、或者对故障下游造成二次冲击？

## A
一是要能限定「只对哪些异常类型重试」（比如只重试网络超时 `TimeoutError`，不重试参数错误 `ValueError`），否则会把编程错误也悄悄重试掉，掩盖真正的 bug；二是要能配置「重试间隔的退避策略」（比如固定间隔或指数退避 exponential backoff），否则对一个持续故障的下游高频重试，只会加重故障、甚至耗尽自己的资源。
