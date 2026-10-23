---
id: hl-j10-java8-two-paths
node: java21.j10-virtual-threads
type: qa
step: 5
---
## Q
Java 8 时代处理大量阻塞请求只有两条路：线程池限流和异步回调。各自的代价是什么？

## A
**路 1：线程池限流。** 例如 `newFixedThreadPool(50)`，任务排队，吞吐被池大小锁死。1000 个各睡 100 ms 的任务，理论 1000 ÷ 50 = 20 批 × 100 ms = 2 秒，实测约 4185 ms（macOS 上 `Thread.sleep(100)` 实际睡约 200 ms）。线程大多在睡觉，CPU 空着，吞吐却上不去。

**路 2：异步回调 / 响应式**（`CompletableFuture`、Netty、Reactor）。线程不阻塞了，但：
- 调用链被切碎，stack trace 只剩回调框架的栈；
- 调试器单步跟不进去；
- `try/catch`、`try-with-resources`、循环都得改写成链式调用；
- 混进一个同步库（如 JDBC 驱动），整条异步链就卡住。
