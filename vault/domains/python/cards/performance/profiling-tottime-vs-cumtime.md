---
id: profiling-tottime-vs-cumtime
node: performance.profiling
type: qa
source: python-docs
---
## Q
`cProfile` 报告里 `tottime` 和 `cumtime` 分别衡量什么？某函数的调用计数显示为 `3/1` 这种两段式数字说明什么？

## A
`tottime` 是函数自身执行耗时，不含它调用的子函数；`cumtime` 是从进入到退出的累计耗时，含所有子调用，对递归函数依然准确。两段式计数 `3/1` 中，前者是总调用次数，后者是「原生调用」（primitive calls）次数，即非递归触发的调用次数。
