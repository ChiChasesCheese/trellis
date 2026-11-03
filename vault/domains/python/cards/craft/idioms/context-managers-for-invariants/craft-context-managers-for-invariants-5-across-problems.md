---
id: craft-context-managers-for-invariants-5-across-problems
node: craft.idioms.context-managers-for-invariants
type: qa
step: 5
---
## Q
**上下文管理器守不变量 · 转账、四子棋、限流器里同一个「进入占、退出放」**｜写法

幂等转账的 `_owning`、四子棋的 `_locked`、限流器的 `reserve` 都是 `@contextmanager`，守的东西各不相同。它们哪里相同，哪里不同？

## A
**要点。** 相同：进入时占住某样东西（键、局锁、分片锁里的状态），`yield` 把它交给业务块，业务块怎么退出都由管理器负责收尾。不同的只是**占的是什么、收的是什么**。

```python
# idempotent-transfer._owning：占的是「键的所有权」，收尾分成败
try:
    yield
except BaseException:
    ...                         # 还没动钱就失败：释放键，允许重试
    raise
finally:
    rec.done.set()              # 先存结果，后唤醒

# connect-four._locked：占的是「这一局的锁」，全局锁只查字典
with self._mu:
    match = self._matches.get(game_id)
with match.lock:
    yield match

# rate-limiter.reserve：占的是「分片里某个 key 的状态」，退出时顺手做摊还回收
with shard.lock:
    state = shard.states.get(key)
    if state is None:
        state = shard.states[key] = self._factory()
    try:
        yield state
    finally:
        if shard.ops >= shard.purge_at:
            self._purge(shard, now)
```

三者的 `yield` 都在 `try` 或 `with` 里面，收尾都在 `finally` 或 `with` 的退出里，所以不管业务块怎么结束都会走到。限流器的 `reserve` 是公开的，是因为组合限流器要借它「先锁住几条规则的状态，再统一决定扣不扣」。

**见于。** idempotent-transfer、connect-four、rate-limiter、airline（`ExitStack` 依次进入多把锁）。

**信号。** 业务函数里出现「开头拿、结尾放」的一对操作，并且中间有多个 `return` 或 `raise`；或者一个临界区被多个入口重复写。
