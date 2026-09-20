---
id: problems-thread-pool-base-exception-in-worker
node: problems.components.thread-pool
type: qa
step: 1
tags: [grown]
---
## Q
线程池的工作线程循环里，捕获任务体抛出的异常时，为什么用 `except BaseException` 而不是更常见的 `except Exception`？

## A
因为『任务异常绝不杀死 worker』这个承诺，如果只用 `Exception` 兜底就留了一个没写进合同的例外：`SystemExit`、`KeyboardInterrupt` 这类继承自 `BaseException` 而不是 `Exception` 的信号，依然会让 worker 线程直接退出，之后所有排队等它执行的任务都不会再有 worker 处理，而调用方完全看不出线程池已经少了一个 worker——它只会发现自己提交的任务永远卡着不完成。标准库 `concurrent.futures` 自己在 worker 内部就是用 `BaseException` 兜底、把它封进对应任务的 `Future`，这里延续这个先例：worker 线程本来就不该响应任务体里意外冒出来的解释器级信号，那应该是主线程的职责。
