---
id: tlc-tt-concurrency-limited-runner-3-why
node: a.tt-concurrency-limited-runner
type: qa
step: 3
---
## Q
**限制并发数的异步任务执行器**｜正确性

用 `Semaphore` 的并发池里，为什么“调用任务”必须写在 `async with sem` 里面、并且放进 `try` 内？给出把它们写错、结果就不对的输入。

## A
**不变量。** 任一时刻，处在 `async with sem` 内的包装协程不超过 `limit` 个；每个任务只在它的包装协程拿到名额后才被调用一次；`results[i]` 只由第 `i` 个包装协程写入。

**为什么。** 名额只约束“进入 `async with` 之后”的代码。任务如果在拿名额之前就被调用（例如先 `coros = [t() for t in tasks]`），启动动作发生在名额之外，上限形同虚设；任务在 `try` 之外被调用，同步抛出的异常就会绕过记录，直接从 `run_limited` 抛出。

**反例一：同步抛出的异常。** 任务列表是 `[f]`，其中 `f` 是普通函数，一被调用就 `raise KeyError("sync")`。写成 `[t() for t in tasks]` 时，`run_limited` 直接抛出 `KeyError`；调用放进 `try` 后得到 `[("rejected", KeyError('sync'))]`。

**反例二：分批。** 把任务切成每 `limit` 个一批、批内 `gather` 的写法，不满足“一个结束立刻补上”。任务 `a` 耗时 50ms，`b`、`c`、`d` 各 10ms，`limit = 2`：分批的日志是 `start a, start b, end b, end a, start c, start d`，`c` 在 `a` 结束后才开始；信号量版是 `start a, start b, end b, start c, end c, start d, end d, end a`，`c` 紧跟着 `b` 开始。
