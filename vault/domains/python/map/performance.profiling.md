%% trellis:begin %%
# 先测量：`timeit`、`cProfile`、采样剖析器与内存剖析
*性能与数据处理*

掌握微基准与整体剖析的区别、`cProfile` 的函数级开销、`py-spy` 类采样器对生产进程的低侵入，以及用 `tracemalloc`/`memray` 看内存。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/python/map/performance.compiling|编译与本地扩展：Cython、Numba、`ctypes` 与何时换引擎]]

## Readings
- [[cpyint-06-debugging-benchmarking|CPython Internals · 调试与基准测试]]
- [[effective-11-performance|Effective Python 3e · 第 11 章 性能]]
- [[hpp-01-understanding-performant-programming|High Performance Python 2e · 第 1 章 理解高性能编程]]
- [[hpp-02-profiling|High Performance Python 2e · 第 2 章 性能分析]]
- [[pydocs-profilers|Python Profilers：cProfile 与 profile]]
- [[pydocs-timeit-module|timeit 模块：微基准测试]]

## Drills
- [[performance-aggregate-50m-rows|Drill：5000 万行 CSV 按 key 求和，四档实现逐级升级]]

## Cards (6)
1. [[profiling-cprofile-clock-tick-limit]]
2. [[profiling-deterministic-vs-sampling]]
3. [[profiling-timeit-disables-gc]]
4. [[profiling-timeit-vs-cprofile-scope]]
5. [[profiling-tottime-vs-cumtime]]
6. [[profiling-tracemalloc-snapshot-diff]]
%% trellis:end %%

## Notes
