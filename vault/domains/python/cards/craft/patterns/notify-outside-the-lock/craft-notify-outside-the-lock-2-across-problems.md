---
id: craft-notify-outside-the-lock-2-across-problems
node: craft.patterns.notify-outside-the-lock
type: qa
step: 2
---
## Q
**锁内记事件、锁外派发 · 熔断器、缓存、证券里同一个派发骨架**｜模式

熔断器的状态变化、TTL 缓存的淘汰、证券的盘口行情，都要通知外部订阅者。三份参考解的派发函数各不相同，哪些部分是同一个机制？每一份在锁内到底留下了什么？

## A
**要点。** 同一个机制：锁内产出「事实」（事件，或订阅者快照），锁外遍历调用。不同点只在锁内留下的东西：一个事件列表、一个订阅者元组，或两者都有。

```python
# api-circuit-breaker._dispatch：换走事件列表
with self._lock:
    events, self._events = self._events, []
for old, new in events:
    try: self._listener(old, new)
    except Exception: _log.exception("on_state_change 回调抛出异常")

# ttl-cache._publish：订阅者在锁内拍成元组
with self._lock:
    listeners = tuple(self._listeners)
for event in events:
    for listener in listeners:
        listener(event)

# stock-brokerage._publish：同样拍快照，事件由撮合时在锁内算好
with self._lock:
    subscribers = tuple(self._subscribers)
for subscriber in subscribers:
    subscriber(event)
```

订阅者列表要拍成元组：遍历期间别的线程订阅或退订，不会改到正在遍历的容器。事件必须是冻结的事实快照（含全部字段），订阅者不用回头查状态。

**见于。** api-circuit-breaker、ttl-cache、stock-brokerage、amazon-locker、amz-file-watcher、elevator。

**信号。** 对象有 `subscribe / on_xxx / listener` 之类的接口，且回调由外部传入；方法里出现 `for cb in self._callbacks: cb(...)` 却还在 `with self._lock` 的缩进里。
