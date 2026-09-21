---
nodes:
- concurrency.executors
title: concurrent.futures：线程池与进程池的统一接口
corpus: python-docs
section: 24-concurrent-futures
url: https://docs.python.org/3/library/concurrent.futures.html
tags:
- canonical
---

# concurrent.futures：线程池与进程池的统一接口

concurrent.futures 给线程池和进程池提供了统一的高层接口，是比直接用 threading/multiprocessing 更省心的选择。Executor.submit() 立即返回一个 Future 对象，真正的结果要调 .result() 才能拿到（如果任务还没完成会阻塞等待，如果任务抛了异常，异常会在这里被重新抛出）；.map() 按提交顺序返回结果（哪怕后提交的先完成也要等前面的），而 as_completed() 则是谁先完成先返回谁，更适合尽快处理完成的任务场景。文档给出的完整示例展示了如何用 with 语句包裹 ThreadPoolExecutor 确保线程池被正确清理。选择 ThreadPoolExecutor 还是 ProcessPoolExecutor 的判断标准很直接：I/O 密集用线程池，CPU 密集用进程池，这是并发选型面试题的标准答案框架。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/concurrent.futures.html)

## Archived copy
![[pydocs-concurrent-futures-clip]]
%% trellis:end %%
