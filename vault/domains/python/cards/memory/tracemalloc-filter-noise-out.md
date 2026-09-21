---
id: tracemalloc-filter-noise-out
node: memory.leaks-tracemalloc
type: qa
source: python-docs
---
## Q
分析 `tracemalloc` 快照时，为什么常常要先用 `snapshot.filter_traces(...)` 把 `<frozen importlib._bootstrap>`、`<unknown>` 这类文件过滤掉？

## A
这些条目对应的是解释器自身导入模块、字节码常量等基础设施开销，几乎在任何程序里都会出现且体量不小，如果不过滤会一直占据 Top N 榜单前列，掩盖真正由业务代码引入的分配热点；先过滤掉这类噪声（noise），剩下的统计结果才能直接指向值得排查的业务代码位置。
