---
id: choosing-cost-per-option
node: concurrency.choosing
type: qa
tags: [grown]
---
## Q
线程、进程、asyncio 这三种并发方案，各自主要付出什么代价？

## A
线程：仍共享同一个 GIL，CPU 密集任务无法真正加速，共享可变状态需要显式加锁，管理不当会死锁或产生竞态。进程：每个进程有独立内存空间，参数和返回值要走 pickle 序列化，跨进程通信有额外开销，内存占用是线程方案的数倍。asyncio：单线程内协作式调度，一旦某个协程执行了同步阻塞调用或纯 CPU 密集计算而不让出控制权，会卡住整条事件循环上所有其他任务，且要求所依赖的 I/O 库有对应的异步实现。
