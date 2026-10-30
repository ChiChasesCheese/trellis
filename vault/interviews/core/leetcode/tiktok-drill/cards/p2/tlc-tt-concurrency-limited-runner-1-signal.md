---
id: tlc-tt-concurrency-limited-runner-1-signal
node: p2.tt-concurrency-limited-runner
type: qa
step: 1
---
## Q
**限制并发数的异步任务执行器**｜Medium · 近一年被问：美国 0 次、国内 7 次 · 最近 2026-10-26（国内面试记录）

实现 `async def run_limited(tasks, limit)`：`tasks` 是 `n` 个无参的异步函数（调用后返回协程，`0 <= n <= 10^5`），同一时刻最多 `limit` 个在执行，一个结束立刻补上下一个，每个任务恰好调用一次。返回与输入顺序一致的结果列表，每项是 `("fulfilled", 值)` 或 `("rejected", 异常)`，任何异常（包括调用时同步抛出的）都只记录、不让整体失败；`limit` 不是正整数时抛 `ValueError`。例：`limit = 2`，第 2 个任务抛 `RuntimeError`，则结果第 2 项是 `("rejected", RuntimeError(...))`，其余项仍是 `("fulfilled", 值)`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「同时最多 `limit` 个、一个结束立刻补上」→ **并发池**（bounded concurrency）：信号量，或固定数量的 worker 抢任务。
- 「返回与输入顺序一致」→ 按**下标**写回 `results[i]`，不能按完成顺序追加。
- 「异常不能让整体失败」→ 每个任务自己 `try/except`；`TaskGroup` 里任何子任务抛出异常都会取消全体，所以异常不能漏出包装函数。
- `n` 到 `10^5`：任务本身是 I/O 等待，调度开销必须是 `O(n)`；一次性并发 `n` 个会撑爆连接或内存。

**推导链。**
1. 逐个 `await`：上限满足，但没有并发，总耗时是所有任务之和。
2. 全部 `gather`：并发数等于 `n`，违反上限。
3. 每 `limit` 个一批 `gather`：慢任务拖住整批，空出来的名额闲着，违反“一个结束立刻补上”。
4. 缺的是**名额**这个概念。`Semaphore(limit)` 就是名额计数器：任务结束归还，队首等待者立刻被唤醒；任务在拿到名额之后才被调用，包装函数里 `try/except Exception` 兜住所有异常。

**同模式的题**：LC 1114 按序打印、LC 1188 设计有限阻塞队列、LC 1226 哲学家进餐；工程里的连接池和并发限流。
