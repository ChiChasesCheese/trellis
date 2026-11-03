%% trellis:begin %%
# 原子占位：检查与占用在同一个临界区（claim, not check-then-act）
*编码功力（Coding Craft） / 跨题模式（Patterns）*

「先查空闲再写占用」永远有竞态；把查和占合成一个锁内的比较并交换，输家得到明确的失败。

**Requires:** [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]], [[domains/python/map/concurrency.gil|全局解释器锁（GIL）：它保护什么、何时释放、切换间隔]]

## Cards (4)
1. [[craft-atomic-claim-check-then-act-1-check-then-act]]
2. [[craft-atomic-claim-check-then-act-2-lost-callback]]
3. [[craft-atomic-claim-check-then-act-3-claim-state-across-problems]]
4. [[craft-atomic-claim-check-then-act-4-db-primitives]]
%% trellis:end %%

## Notes
