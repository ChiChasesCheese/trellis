---
id: choosing-threads-vs-asyncio-io
node: concurrency.choosing
type: qa
tags: [grown]
---
## Q
同样是 I/O 密集任务，什么情况下用线程比用 asyncio 更合适？

## A
当要调用的 I/O 库本身是同步阻塞的（没有 `async`/`await` 版本，比如很多传统数据库驱动、旧版 SDK）时用线程：线程可以直接调用这些阻塞函数，靠线程切换重叠等待时间；用 asyncio 则必须要求整条调用链上的每一层都是异步实现，否则一次同步阻塞调用会卡住整个单线程事件循环，反而让所有并发任务一起卡住。改造遗留同步库为异步往往成本很高，这时线程池（哪怕效率不如 asyncio）是更现实的选择。
