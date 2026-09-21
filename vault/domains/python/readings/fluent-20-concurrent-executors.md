---
nodes: [concurrency.executors]
url: https://www.fluentpython.com/
tags: [book, no-archive]
title: Fluent Python 2e · 第 20 章 并发执行者
---
# Fluent Python 2e · 第 20 章 并发执行者

这一章讲 `concurrent.futures` 提供的 `ThreadPoolExecutor`/`ProcessPoolExecutor` 如何用统一的 `Future`/`submit`/`map` 接口屏蔽线程池和进程池的差异，让调用方代码基本不用改。

**读时提取：**
- `Executor.submit` 返回 `Future`，`Future.result()` 如何阻塞等待结果
- `ThreadPoolExecutor` 与 `ProcessPoolExecutor` 共享同一套接口，切换成本很低
- `as_completed` 与 `map` 两种收集结果方式的适用场景差异

%% trellis:begin %%
## Source
[Open the original ↗](https://www.fluentpython.com/)
%% trellis:end %%
