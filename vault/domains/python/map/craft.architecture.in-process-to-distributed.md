%% trellis:begin %%
# 从单进程到分布式：每个原语在生产里换成什么
*编码功力（Coding Craft） / 架构理解（Architecture）*

锁、Condition、堆、字典、日志、时钟，各自在分布式里有对应物；哪些保证会丢，用什么补。

**Requires:** [[domains/python/map/concurrency.choosing|选型：I/O 密集 vs CPU 密集、线程 / 进程 / asyncio 的决策树]], [[domains/python/map/concurrency.multiprocessing|多进程：`multiprocessing`、fork vs spawn、pickle 边界与共享内存]]

## Cards (5)
1. [[craft-in-process-to-distributed-1-who-provides-atomic]]
2. [[craft-in-process-to-distributed-2-clocks-do-not-agree]]
3. [[craft-in-process-to-distributed-3-rate-limit-options]]
4. [[craft-in-process-to-distributed-4-log-and-offsets]]
5. [[craft-in-process-to-distributed-5-ids-and-what-is-lost]]
%% trellis:end %%

## Notes
