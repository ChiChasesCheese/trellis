%% trellis:begin %%
# 调用方向与可重入：谁能调谁，回调时手里不能有锁
*编码功力（Coding Craft） / 架构理解（Architecture）*

整个调用图画成单向的层次：服务→池→对象，下层从不回调上层；观察者永远在锁外被调用。

**Requires:** [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]]

## Cards (5)
1. [[craft-lock-hierarchy-and-reentrancy-1-callback-under-lock]]
2. [[craft-lock-hierarchy-and-reentrancy-2-one-direction]]
3. [[craft-lock-hierarchy-and-reentrancy-3-intentional-rlock]]
4. [[craft-lock-hierarchy-and-reentrancy-4-notify-outside]]
5. [[craft-lock-hierarchy-and-reentrancy-5-service-call-graph]]
%% trellis:end %%

## Notes
