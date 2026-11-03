%% trellis:begin %%
# 上下文管理器守不变量：@contextmanager 与 ExitStack
*编码功力（Coding Craft） / 高级写法（Idioms）*

把「获取—使用—善后」写成 with：每个出口都做对的收尾，调用方不用记得 try/finally。

**Requires:** [[domains/python/map/iteration.context-managers|上下文管理器：`__enter__`/`__exit__`、`contextlib.contextmanager` 与 `ExitStack`]], [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]]

## Cards (6)
1. [[craft-context-managers-for-invariants-1-cleanup-in-one-place]]
2. [[craft-context-managers-for-invariants-2-must-reraise]]
3. [[craft-context-managers-for-invariants-3-narrow-global-lock]]
4. [[craft-context-managers-for-invariants-4-exitstack]]
5. [[craft-context-managers-for-invariants-5-across-problems]]
6. [[craft-context-managers-for-invariants-6-scales-transaction-lease]]
%% trellis:end %%

## Notes
