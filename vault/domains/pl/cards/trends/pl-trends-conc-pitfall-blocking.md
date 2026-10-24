---
id: pl-trends-conc-pitfall-blocking
node: trends.concurrency-evolution
type: qa
step: 10
---
## Q
并发模型在生产中最常见的失败是什么？Python 的“在协程里阻塞”和“野生任务”、Java 的“线程耗尽”分别是什么样子？

## A
**失败一：在事件循环里阻塞（Python、Rust async、JavaScript）**。三个任务并发，每个调用阻塞的 `time.sleep(1)`（或同步的数据库驱动、`requests.get`、CPU 密集计算）：

```python
async def bad(): time.sleep(1)          # blocks the event loop
await asyncio.gather(bad(), bad(), bad())
```

真实输出：总共 **3.4 秒**，而 `await asyncio.sleep(1)` 版本是 1.0 秒。症状：整个服务的延迟曲线周期性出现尖刺，连健康检查都超时，因为事件循环被一个任务占住，其他几千个连接都在等。

**失败二：野生任务（任何语言）**。后台任务忘了等待和取消：请求被客户端取消后，后台的数据库查询继续运行；任务里抛的异常无人处理，被默默丢弃（Python 的 `create_task` 返回值没被保存，异常变成“Task exception was never retrieved”日志）。内存里堆积越来越多没人管的任务。用 `TaskGroup` 或 `errgroup`，让任务属于某个作用域。

**失败三：线程耗尽（Java 平台线程）**。每请求一线程的服务，下游变慢，线程全部卡在等待，池满，新请求排队或被拒绝，进而级联故障。本机复现：5000 个各自睡眠 1 秒的任务提交给缓存线程池，真实结果是 `OutOfMemoryError: unable to create native thread`。改用虚拟线程后，十万个任务约 1.5 秒完成。

**失败四：虚拟线程被钉住（Java）**。在 `synchronized` 块里做阻塞 I/O，虚拟线程无法卸载，占着载体系统线程，吞吐退回到平台线程水平。用 `ReentrantLock` 替代。

**共同点**：新模型降低了创建成本，却没有取消“资源总是有限”的事实。**必须自己限制并发度、设置超时、保证取消传播**。

**防线**：压测时模拟下游变慢，观察是排队、拒绝还是崩溃；监控事件循环延迟、线程池队列长度、活跃任务数；代码评审时问“这个任务由谁等待、由谁取消”。
