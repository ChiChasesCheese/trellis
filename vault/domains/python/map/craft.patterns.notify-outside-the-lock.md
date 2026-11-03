%% trellis:begin %%
# 锁内记事件、锁外派发（collect under lock, dispatch outside）
*编码功力（Coding Craft） / 跨题模式（Patterns）*

状态变化在锁内完成并记录事件；回调订阅者在释放锁之后。慢订阅者或回头调用本对象的订阅者就不会死锁。

**Requires:** [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]], [[domains/python/map/classes.dataclasses|`dataclass`、`NamedTuple` 与 `__slots__`]]

## Cards (5)
1. [[craft-notify-outside-the-lock-1-collect-then-dispatch]]
2. [[craft-notify-outside-the-lock-2-across-problems]]
3. [[craft-notify-outside-the-lock-3-future-callbacks]]
4. [[craft-notify-outside-the-lock-4-stale-event]]
5. [[craft-notify-outside-the-lock-5-scales-outbox]]
%% trellis:end %%

## Notes
