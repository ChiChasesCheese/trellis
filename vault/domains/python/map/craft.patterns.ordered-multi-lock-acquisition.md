%% trellis:begin %%
# 按全局固定顺序拿多把锁（lock ordering）
*编码功力（Coding Craft） / 跨题模式（Patterns）*

需要同时持有多把锁时，按稳定的全局顺序（账户 id、实例 key）进入，不按参数顺序。

**Requires:** [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]]

## Cards (5)
1. [[craft-ordered-multi-lock-acquisition-1-abba-deadlock]]
2. [[craft-ordered-multi-lock-acquisition-2-exitstack]]
3. [[craft-ordered-multi-lock-acquisition-3-hidden-precondition]]
4. [[craft-ordered-multi-lock-acquisition-4-layer-discipline]]
5. [[craft-ordered-multi-lock-acquisition-5-scales-row-locks]]
%% trellis:end %%

## Notes
