%% trellis:begin %%
# 性能与数据处理

先测量再优化：剖析工具、内建容器的性能特征、NumPy 向量化与内存布局、pandas 在百万行以上的正确用法，以及何时用编译或换引擎。

## Topics
- [[domains/python/map/performance.profiling|先测量：`timeit`、`cProfile`、采样剖析器与内存剖析]]
- [[domains/python/map/performance.containers|内建容器的性能：list 追加/插入、dict/set 查找、deque 与 bisect]]
- [[domains/python/map/performance.numpy-vectorization|NumPy 向量化与内存布局：ndarray、广播、连续内存与视图]]
- [[domains/python/map/performance.pandas-at-scale|pandas 大表：分块读取、dtype 与 category、`groupby` 与合并、写时复制]]
- [[domains/python/map/performance.compiling|编译与本地扩展：Cython、Numba、`ctypes` 与何时换引擎]]
- [[domains/python/map/performance.less-ram|省内存：生成器、`array`、`memoryview`、`__slots__` 与稀疏结构]]
%% trellis:end %%

## Notes
