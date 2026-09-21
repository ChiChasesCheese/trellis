---
id: profiling-deterministic-vs-sampling
node: performance.profiling
type: qa
source: python-docs
---
## Q
`cProfile` 这类确定性剖析（deterministic profiling）和 `py-spy` 这类采样剖析器（sampling/statistical profiler）在机制上有什么根本区别，各自的代价是什么？

## A
确定性剖析给每次函数调用/返回/异常都挂钩子精确计时，结果精确但开销随调用次数增长，且要在被测进程内插桩；采样剖析器按固定间隔随机读取当前调用栈，不需要改动或注入目标代码，开销低到可以直接挂在生产进程上，但只能给出相对的热点分布，不是精确耗时。
