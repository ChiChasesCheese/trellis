---
id: problems-pub-sub-overflow-policy-three
node: problems.components.pub-sub
type: qa
step: 4
tags: [grown]
---
## Q
进程内 Pub-Sub 的主题保留日志写满了，有哪三种溢出策略？各自的代价是什么？默认该选哪个？

## A
- `DROP_OLDEST`（丢最旧）：发布者永不阻塞，直接淘汰队头。代价是落后的订阅者会少看一段，因此**必须**配一个可读的丢失计数，否则就是静默丢数据。
- `BLOCK`（阻塞发布者）：一条不丢，代价是**最慢的一个订阅者会反压住所有发布者**，一个卡死的订阅者等于整条总线卡死——所以 `publish` 必须带超时。
- `REJECT`（拒绝发布）：发布者立刻拿到背压（backpressure）异常，自己决定降级、采样还是重试。适合『宁可不发也不许拖慢主流程』的埋点、审计。

进程内事件总线默认选 `DROP_OLDEST`：它服务的是解耦而不是账目，拖慢业务线程的代价比丢几条监控事件大得多。谁要不丢，谁在建主题时把策略换成 `BLOCK`。三种取舍写成一个 `Enum` 放在主题上，而不是在 `append` 里写死一句 `popleft()`。
