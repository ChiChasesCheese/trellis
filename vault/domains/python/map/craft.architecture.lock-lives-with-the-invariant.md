%% trellis:begin %%
# 锁跟着不变量走：谁拥有不变量，谁拥有锁（aggregate owns its lock）
*编码功力（Coding Craft） / 架构理解（Architecture）*

一个不变量涉及哪些数据，就把它们放进同一个对象并由同一把锁保护；服务层只保护目录。

**Requires:** [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]]

## Cards (4)
1. [[craft-lock-lives-with-the-invariant-1-lock-beside-the-data]]
2. [[craft-lock-lives-with-the-invariant-2-owner-of-cursors]]
3. [[craft-lock-lives-with-the-invariant-3-entity-without-lock]]
4. [[craft-lock-lives-with-the-invariant-4-partition-as-lock]]
%% trellis:end %%

## Notes
