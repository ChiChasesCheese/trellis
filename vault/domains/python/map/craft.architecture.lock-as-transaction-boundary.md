%% trellis:begin %%
# 一把锁就是一个事务：临界区边界 = 原子性边界
*编码功力（Coding Craft） / 架构理解（Architecture）*

单进程里，一把锁圈住的区间就是数据库事务的替身：检查、修改、写日志要么都在里面，要么都不在。

**Requires:** [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]], [[domains/python/map/concurrency.choosing|选型：I/O 密集 vs CPU 密集、线程 / 进程 / asyncio 的决策树]]

## Cards (4)
1. [[craft-lock-as-transaction-boundary-1-lock-is-the-boundary]]
2. [[craft-lock-as-transaction-boundary-2-what-the-lock-becomes]]
3. [[craft-lock-as-transaction-boundary-3-external-calls]]
4. [[craft-lock-as-transaction-boundary-4-one-coarse-lock]]
%% trellis:end %%

## Notes
