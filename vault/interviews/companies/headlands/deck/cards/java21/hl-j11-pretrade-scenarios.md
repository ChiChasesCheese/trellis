---
id: hl-j11-pretrade-scenarios
node: java21.j11-structured-concurrency
type: qa
step: 13
---
## Q
下单前并行检查的三个场景（全部成功、风控 100 ms 失败而行情要 1500 ms、行情 3000 ms 而 deadline 400 ms）各是什么结果？和 Java 8 写法比好在哪？

## A
- **全部成功**：返回合并结果。三个子任务的完成顺序由调度和 sleep 精度决定，**别依赖子任务完成顺序**。
- **风控 100 ms 失败**：scope shutdown → 还在 sleep 的行情收到中断被取消 → `main` 立刻拿到 `ExecutionException`，**不用等 1500 ms**（Java 8 的写法等了 1.5 秒）。
- **行情太慢**：`joinUntil` 超时抛 `TimeoutException`，抛出前 scope 已 shutdown，慢的行情被取消。

好处：失败快速传播、慢任务被取消、块结束时线程一定已结束。
