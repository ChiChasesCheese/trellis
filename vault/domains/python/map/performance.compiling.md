%% trellis:begin %%
# 编译与本地扩展：Cython、Numba、`ctypes` 与何时换引擎
*性能与数据处理*

理解把热点编译为 C 的三条路径与各自的代价、NumPy/Numba 释放 GIL 的条件，以及"把计算推给 DuckDB/SQL 引擎"往往比优化 Python 循环更划算。

**Requires:** [[domains/python/map/performance.profiling|先测量：`timeit`、`cProfile`、采样剖析器与内存剖析]]

## Readings
- [[effective-11-performance|Effective Python 3e · 第 11 章 性能]]
- [[hpp-07-compiling-to-c|High Performance Python 2e · 第 7 章 编译为 C]]

## Drills
- [[performance-aggregate-50m-rows|Drill：5000 万行 CSV 按 key 求和，四档实现逐级升级]]

## Cards (6)
1. [[compiling-cython-needs-type-annotations]]
2. [[compiling-gil-release-condition]]
3. [[compiling-numba-jit-warmup-cost]]
4. [[compiling-numba-object-mode-fallback]]
5. [[compiling-push-down-to-duckdb-sql]]
6. [[compiling-three-paths-to-c]]
%% trellis:end %%

## Notes
