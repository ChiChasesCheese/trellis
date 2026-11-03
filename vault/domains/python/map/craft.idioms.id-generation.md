%% trellis:begin %%
# ID 生成：itertools.count、next 与生成器表达式的陷阱
*编码功力（Coding Craft） / 高级写法（Idioms）*

用 next(itertools.count(1)) 生成单调 ID；不要把它包进生成器表达式在锁外共享。

**Requires:** [[domains/python/map/iteration.generators|生成器函数与生成器表达式：惰性、O(1) 内存与一次性]], [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]], [[domains/python/map/concurrency.gil|全局解释器锁（GIL）：它保护什么、何时释放、切换间隔]]

## Cards (4)
1. [[craft-id-generation-1-counter-not-len]]
2. [[craft-id-generation-2-formatting-is-not-a-limit]]
3. [[craft-id-generation-3-caller-supplies-the-id]]
4. [[craft-id-generation-4-scales-snowflake]]
%% trellis:end %%

## Notes
