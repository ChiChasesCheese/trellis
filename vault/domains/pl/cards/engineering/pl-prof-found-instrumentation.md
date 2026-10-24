---
id: pl-prof-found-instrumentation
node: engineering.profiling
type: qa
step: 3
---
## Q
插桩式剖析（instrumenting profiler）怎样工作？Python 的 `cProfile` 给出什么，代价是什么，什么时候该用它？

## A
**机制**：运行时在每次函数调用和返回时执行一个钩子，读时间戳并累加。它不靠概率，所以调用次数是精确的，也不会漏掉比采样间隔还短的函数。`cProfile` 是 CPython 标准库里的这种剖析器。

输出（对一个循环 300 万次调用小函数 `tiny` 的程序）：

```text
3000002 function calls in 0.198 seconds
ncalls  tottime  percall  cumtime  percall  filename:lineno(function)
     1    0.136    0.136    0.198    0.198  t.py:6(work)
3000000    0.062    0.000    0.062    0.000  t.py:3(tiny)
```

`tottime` 是函数自身耗时（对应采样里的 `flat`），`cumtime` 是含子调用的耗时（对应 `cum`），`ncalls` 是精确次数。

**代价**：同一段代码不加剖析是 0.04 s，加了 `cProfile` 是 0.20 s，约 5 倍（本机一次测量）。原因是每次调用都要付一份固定的钩子开销：函数越小、调用越频繁，被放大得越厉害，而大函数几乎不受影响。于是插桩剖析会把排名扭曲成「调用次数多的小函数最慢」。

**什么时候用**：需要精确的调用次数和调用关系（「这个函数被调了 300 万次」往往直接暴露算法问题），代码量小的离线分析。不要在生产环境常开，也不要拿它的绝对耗时和未剖析的运行比较；要看真实占比，用采样式。
