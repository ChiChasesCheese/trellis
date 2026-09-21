---
id: profiling-timeit-vs-cprofile-scope
node: performance.profiling
type: qa
source: python-docs
---
## Q
用 `timeit` 测量一段 Python 代码的执行时间，和用 `cProfile` 剖析整个程序，两者为什么不能互相替代？

## A
`timeit`（微基准，microbenchmark）反复执行同一条语句并取最快一次，专门排除系统噪声，适合比较几种写法的相对速度；`cProfile` 是整体剖析器（profiler），给程序里每个函数打点计数与计时，适合定位「热点在哪」而不是精确测某一行的绝对耗时——一个求多快，一个求哪里慢。
