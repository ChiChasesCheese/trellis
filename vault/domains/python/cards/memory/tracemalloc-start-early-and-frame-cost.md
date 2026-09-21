---
id: tracemalloc-start-early-and-frame-cost
node: memory.leaks-tracemalloc
type: qa
source: python-docs
---
## Q
为什么建议尽可能早地启动 `tracemalloc`（例如用 `PYTHONTRACEMALLOC=1` 环境变量或 `-X tracemalloc` 启动参数，而不是等程序跑了一会儿再调用 `tracemalloc.start()`）？

## A
`tracemalloc` 只能追踪它开始运行之后发生的内存分配；越晚启动，越可能错过程序早期（如模块导入阶段）就发生的分配，导致后续快照里看不到这部分内存是从哪来的。启动越早，能追踪到的分配就越完整，代价是默认只保存 1 帧调用栈以控制开销，需要更详细的调用链时再显式加大保存帧数（同时增加追踪本身的开销）。
