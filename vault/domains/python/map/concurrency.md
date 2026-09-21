%% trellis:begin %%
# 并发模型：GIL、线程与进程

理解 GIL 决定了线程适合 I/O 而非 CPU，进程绕过 GIL 但付出序列化代价，以及标准库提供的同步原语、执行器与 3.13 自由线程（free-threading）的现状。

## Topics
- [[domains/python/map/concurrency.gil|全局解释器锁（GIL）：它保护什么、何时释放、切换间隔]]
- [[domains/python/map/concurrency.threads|线程：`threading.Thread`、守护线程与线程适用的场景]]
- [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]]
- [[domains/python/map/concurrency.queues|`queue.Queue` 与生产者-消费者：用队列把状态收敛到一个线程]]
- [[domains/python/map/concurrency.multiprocessing|多进程：`multiprocessing`、fork vs spawn、pickle 边界与共享内存]]
- [[domains/python/map/concurrency.executors|`concurrent.futures`：`ThreadPoolExecutor` vs `ProcessPoolExecutor`、`map` 与 `as_completed`]]
- [[domains/python/map/concurrency.free-threading|自由线程（PEP 703，3.13 实验版）与子解释器（PEP 734）]]
- [[domains/python/map/concurrency.choosing|选型：I/O 密集 vs CPU 密集、线程 / 进程 / asyncio 的决策树]]
%% trellis:end %%

## Notes
