---
id: tracemalloc-traceback-pinpoints-allocation-site
node: memory.leaks-tracemalloc
type: qa
source: python-docs
---
## Q
`tracemalloc` 除了统计「哪一行分配了多少内存」，还能定位到具体是被哪个调用链创建的吗？

## A
能。调用 `snapshot.statistics('traceback')` 得到的每条统计带一个 `traceback` 属性，记录了该内存块分配时的调用栈（call stack）；默认只保留最近 1 帧，需要更完整的调用链要在启动时加大保留帧数（如 `tracemalloc.start(25)`），这样才能看清一个内存块究竟是从哪条函数调用路径一路走到这行分配代码的。
