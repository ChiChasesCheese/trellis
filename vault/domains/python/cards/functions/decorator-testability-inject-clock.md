---
id: decorator-testability-inject-clock
node: functions.decorator-patterns
type: qa
tags: [grown]
---
## Q
给 retry/限流装饰器写单元测试时，如果装饰器内部直接调用 `time.sleep()`、`time.time()`，会带来什么麻烦？常见的解决办法是什么？

## A
直接调用真实的 `time.sleep` 会让测试变慢（真的要等上几秒甚至几十秒），直接调用 `time.time()` 又让「有没有超出限流窗口」这类判断依赖真实时钟，测试结果不确定、容易随机失败（flaky）。常见做法是把「休眠函数」和「取当前时间的函数」都做成装饰器的可选参数（默认用 `time.sleep`/`time.monotonic`），测试时注入一个假的、可控前进的时钟或立即返回的休眠函数，让测试在毫秒级、确定性地跑完整个重试/限流逻辑。
