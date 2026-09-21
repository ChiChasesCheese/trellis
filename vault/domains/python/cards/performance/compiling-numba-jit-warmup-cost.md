---
id: compiling-numba-jit-warmup-cost
node: performance.compiling
type: qa
tags: [grown]
---
## Q
用 `@numba.njit` 装饰一个函数后，第一次调用为什么会比后续调用慢很多？这对写微基准测试（microbenchmark）有什么提醒？

## A
Numba 是即时编译（JIT，just-in-time compilation）：第一次调用时才会根据实参的具体类型把函数编译成机器码，这次调用同时承担了编译和执行两部分耗时；之后同类型参数的调用直接复用已编译好的机器码，只剩纯执行耗时。测量 Numba 函数性能必须先「预热」（warm-up，先调用一次让它编译完）再计时，否则会把编译开销错算进执行时间里。
