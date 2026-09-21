---
nodes:
- performance.profiling
title: timeit 模块：微基准测试
corpus: python-docs
section: 62-timeit
url: https://docs.python.org/3/library/timeit.html
tags:
- canonical
---

# timeit 模块：微基准测试

timeit 是专门为这一小段代码到底哪种写法更快设计的微基准测试工具，和分析整个程序哪里慢的 cProfile 定位完全不同，timeit 关心的是单条语句或小函数在大量重复执行下的平均耗时，cProfile 关心的是一整个程序运行过程中每个函数各占用了多少时间。文档给出了命令行用法和 Python API 两种方式，并特别提醒微基准测试容易踩的坑：默认会关闭垃圾回收以减少测量噪声，但这和真实生产环境的运行条件不完全一致，结果只能用来做写法 A 和写法 B 相对谁快的横向比较，不能直接当作生产环境的绝对耗时预期。这是回答这两种写法哪个快这类问题时该动手验证而不是凭感觉回答的正确工具。

%% trellis:begin %%
## Source
[Open the original ↗](https://docs.python.org/3/library/timeit.html)

## Archived copy
![[pydocs-timeit-module-clip]]
%% trellis:end %%
