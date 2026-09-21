---
id: gil-switch-interval
node: concurrency.gil
type: qa
source: python-docs
---
## Q
`sys.getswitchinterval()` 默认返回多少，它控制什么？

## A
默认 5 毫秒（0.005 秒）。它是解释器给并发运行的线程分配的“时间片”理想时长：一个线程执行到这个时长后会被要求让出 GIL，但实际让出时机可能更晚（长时间不含字节码边界的内建调用会推迟），且哪个线程真正被调度运行由操作系统决定，解释器本身没有调度器。可用 `sys.setswitchinterval()` 调整。
