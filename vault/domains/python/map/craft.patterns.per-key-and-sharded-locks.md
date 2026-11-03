%% trellis:begin %%
# 每个对象一把锁与分片锁：把竞争限制在真正冲突的范围
*编码功力（Coding Craft） / 跨题模式（Patterns）*

全局锁只用于查表；每局/每场次/每航班实例持有自己的锁。key 数量巨大时用固定数量的分片锁。

**Requires:** [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]], [[domains/python/map/concurrency.gil|全局解释器锁（GIL）：它保护什么、何时释放、切换间隔]]

## Cards (5)
1. [[craft-per-key-and-sharded-locks-1-lock-per-object]]
2. [[craft-per-key-and-sharded-locks-2-registry-then-object]]
3. [[craft-per-key-and-sharded-locks-3-sharded]]
4. [[craft-per-key-and-sharded-locks-4-shared-state-bug]]
5. [[craft-per-key-and-sharded-locks-5-scales-hash-stability]]
%% trellis:end %%

## Notes
