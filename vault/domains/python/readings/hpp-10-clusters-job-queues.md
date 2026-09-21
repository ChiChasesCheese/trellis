---
nodes: [concurrency.choosing]
url: https://www.oreilly.com/library/view/high-performance-python/9781492055013/
tags: [book, no-archive]
title: High Performance Python 2e · 第 10 章 集群与任务队列
---
# High Performance Python 2e · 第 10 章 集群与任务队列

这一章把并行从单机扩展到集群：用任务队列（如 Celery 类工具）把工作项分发到多台机器，讨论了什么时候单机多进程已经够用、什么时候真的需要跨机器扩展。

**读时提取：**
- 单机多进程和跨机器集群该按什么信号切换（CPU 是否已经打满、数据是否能分片）
- 任务队列如何解耦『提交任务』和『执行任务』，方便水平扩展 worker

%% trellis:begin %%
## Source
[Open the original ↗](https://www.oreilly.com/library/view/high-performance-python/9781492055013/)
%% trellis:end %%
