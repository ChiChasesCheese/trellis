---
nodes:
- concurrency.multiprocessing
title: multiprocessing 模块：绕开 GIL 的真并行
corpus: python-docs
section: 23-multiprocessing
url: https://docs.python.org/3/library/multiprocessing.html
tags:
- canonical
---

# multiprocessing 模块：绕开 GIL 的真并行

multiprocessing 用独立的操作系统进程绕开 GIL 实现真正的并行计算，代价是进程间不共享内存，传参和返回值都必须能被 pickle 序列化。文档系统讲了三种启动方式的取舍：fork（Unix 默认，速度快但在多线程程序里继承锁状态可能导致死锁，且 3.14 起不再是默认）、spawn（跨平台安全、3.14 起的新默认，但启动慢且要求代码在模块级别的 main 保护块下）、forkserver（折中方案）。进程间通信靠 Pipe、Queue，共享状态则靠 shared_memory 或更重的 Manager（后者用代理对象模拟共享数据结构，牺牲性能换取易用性）。这篇文档能回答多线程和多进程该怎么选的下一层问题：选了多进程之后，启动方式和进程间通信手段又该怎么权衡，这是 CPU 密集任务落地时绕不开的实操细节。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/multiprocessing.html)

## Archived copy
![[pydocs-multiprocessing-module-clip]]
%% trellis:end %%
