---
nodes:
- asyncio.coroutines-tasks
- asyncio.cancellation
- asyncio.gather-wait-timeout
- asyncio.blocking-and-threads
title: asyncio：协程与任务完整参考
corpus: python-docs
section: 28-asyncio-task
url: https://docs.python.org/3/library/asyncio-task.html
tags:
- canonical
---

# asyncio：协程与任务完整参考

这是 asyncio 高层 API 里信息密度最高的一篇：协程对象必须被 await 或者用 create_task() 包装成 Task 才会真正开始执行，create_task() 会立即把协程加入事件循环调度，而单纯创建协程对象什么都不会发生，忘记 await 会触发 coroutine was never awaited 警告。文档系统讲了取消机制：task.cancel() 会在任务下一次 await 处注入 CancelledError，asyncio.shield() 可以保护关键代码段不被外部取消打断。3.11 引入的 TaskGroup 提供了结构化并发，组内任何一个任务失败，其余任务会被自动取消，最后用异常组（ExceptionGroup）汇总所有失败原因，比手写 gather() 更安全。还讲了如何用 asyncio.to_thread() 把阻塞调用丢进线程池而不卡住事件循环。这篇文档基本覆盖了写 asyncio 业务代码日常会用到的全部 API。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/asyncio-task.html)

## Archived copy
![[pydocs-asyncio-coroutines-tasks-clip]]
%% trellis:end %%
