---
id: hl-javaq-f-q32-tpe-order
node: java-questions.f-concurrency
type: qa
step: 25
---
## Q
`ThreadPoolExecutor` 接到任务后的处理顺序是什么？为什么无界队列会让 `maximumPoolSize` 失效？还有哪些工程细节要注意？

## A
- **行为顺序**：先到 core 线程数，再入队，**队满才扩到 max**，再满才拒绝。
- 无界队列永远不会满，所以 max 永远不起作用。
- 参数：core / max / 队列 / 拒绝策略。
- 细节：给线程命名（便于 `jstack` / `jcmd Thread.print`）、处理未捕获异常、`Future.get()` 加超时、正确关闭（`shutdown` + `awaitTermination`）。
- ForkJoinPool 与并行 Stream 共用 `commonPool`；别在里面做阻塞 I/O。
- 热路径：线程数 = 绑核数，每线程独占一个核，不用池。
