---
id: profiling-timeit-disables-gc
node: performance.profiling
type: qa
source: python-docs
---
## Q
`timeit.Timer.timeit()` 默认会对垃圾回收（garbage collection，GC）做什么？为什么这样设计，什么情况下要撤销这个默认行为？

## A
默认在计时期间临时关闭 GC，让多次独立测量之间更可比，避免某次测量恰好撞上一次 GC 停顿而失真；但如果被测代码的性能本身依赖 GC（例如频繁产生循环引用），应在 `setup` 参数里先执行 `gc.enable()` 恢复，否则测出的是「无 GC 干扰」的理想值而非真实值。
