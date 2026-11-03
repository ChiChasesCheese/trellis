%% trellis:begin %%
# 装饰器做横切关注点：@_synchronized / @_op 与 functools.wraps
*编码功力（Coding Craft） / 高级写法（Idioms）*

整个方法体都是临界区时，把锁（和「先结清过期」）写在方法头的装饰器里，不会漏一个方法。

**Requires:** [[domains/python/map/functions.decorators|装饰器：`@` 语法糖、`functools.wraps` 与执行时机]], [[domains/python/map/functions.decorator-patterns|带参数的装饰器、类装饰器与常见实例（retry、memoize、timing、rate limit）]], [[domains/python/map/concurrency.locks-races|竞态条件与同步原语：`Lock`、`RLock`、`Condition`、`Event`、`Semaphore`]]

## Cards (5)
1. [[craft-decorators-for-cross-cutting-locks-1-lock-in-the-header]]
2. [[craft-decorators-for-cross-cutting-locks-2-wraps-and-paramspec]]
3. [[craft-decorators-for-cross-cutting-locks-3-whole-method-and-rlock]]
4. [[craft-decorators-for-cross-cutting-locks-4-across-problems]]
5. [[craft-decorators-for-cross-cutting-locks-5-scales-middleware]]
%% trellis:end %%

## Notes
