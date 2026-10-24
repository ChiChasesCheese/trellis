---
id: pl-conc-async-await-best-practice
node: concurrency.async-await
type: qa
step: 7
---
## Q
在 Python asyncio 和 Rust tokio 里写 async 服务，资深工程师遵守哪些规则？什么时候根本不该用 async？

## A
一个事件循环线程同时服务成千上万个任务，所以规则围绕「别占住循环」和「别无限增长」：

1. **循环里不阻塞。** 阻塞 I/O、`time.sleep`、长计算、持锁等待都放到线程池：Python `asyncio.to_thread` / `run_in_executor`，tokio `spawn_blocking`。CPU 密集用进程池或 rayon，不要写在协程里。
2. **每个外部调用都带超时。** 一个没有超时的 `await` 就是一个可能永远挂着的任务。Python `asyncio.timeout`，tokio `timeout`。
3. **并发度有上界。** 一次 `gather` 10 万个请求会瞬间打满下游；用 `asyncio.Semaphore`、tokio `Semaphore` 或有界 channel 限流。
4. **任务要有主人。** Python 用 `TaskGroup`，tokio 用 `JoinSet`，保证子任务出错时其他任务被取消，不留孤儿任务（事件循环只持有任务的弱引用，`create_task` 之后不保存返回值，任务可能被垃圾回收）。
5. **取消要写成可安全的。** Python 里别吞掉 `CancelledError`；Rust 里 `await` 点被丢弃就是取消，持有的资源靠 `Drop` 释放，所以不要在两个 `await` 之间留下半完成的状态。
6. **颜色边界收窄**：把异步代码集中在 I/O 层，业务逻辑保持同步纯函数，便于测试。

**什么时候不用 async**：任务数不大（几十到几百），线程池就够，代码更简单；CPU 密集；团队不熟悉。同步代码出问题能看到完整调用栈，async 出问题常常只看到事件循环。Java 与 Go 用户则几乎不需要这一整套。
