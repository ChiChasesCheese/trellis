---
id: concurrency-asyncio-event-loop
node: concurrency.asyncio
type: qa
step: 1
---
## Q
`asyncio` 的事件循环（event loop）是什么，它和 `threading` 的并发模型根本区别在哪？

## A
事件循环是一个单线程里的调度器：它维护一堆"协程/任务"，每次挑一个正在就绪（不再等待）的任务运行，运行到这个任务主动让出（`await` 一个还没完成的东西）为止，再切到下一个就绪任务，如此循环。整个过程只有一个线程在跑 Python 代码，任务之间的切换点完全由代码自己用 `await` 显式声明，而不是像 `threading` 那样由操作系统在任意字节码之间抢占式地切换。

这个区别是 `asyncio` 并发安全性的根基：正因为切换点是显式、可预测的，一大类 `threading` 下的竞态在纯协程代码里天然不存在——但代价是一旦某个协程不 `await`、一直占着 CPU 算，其他所有协程都得等着，不像线程那样会被操作系统强制切走。
